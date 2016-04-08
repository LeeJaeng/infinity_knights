from app import api_root, access_token_required, db
from app.models.league_duel_history import LeagueDuelHistoryModel
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.metadata.league import MetadataLeagueModel
from app.util.league import get_league_opponent
from app.util.set_user_achievement_value import accrue_user_achievement_value
from flask.ext.restful import Resource, abort, request
from sqlalchemy import func

"""
    # API : 리그 결투 종료
    # DESCRIPTION
        # 등록 된 리그 히스토리에 결과 등록
        # 누적 리그 승리 업적 추가
        # 승리 시 보상 제공
        # 다음 상대 찾은 후 히스토리에 등록

"""


@api_root.resource('/v1/leagues/duels/<int:league_id>/duel-finish')
class LeagueDuelFinish(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        if 'result' not in request.args:
            abort(400)
        # ticket 감소
        league_user_property = LeagueUserPropertyModel.query. \
            filter(LeagueUserPropertyModel.league_id == league_id). \
            filter(LeagueUserPropertyModel.user_id == request_user.id). \
            first()
        if league_user_property is None:
            abort(500)

        if league_user_property.ticket <= 0:
            return {
                'success': False,
                'message': 'not enough ticket'
            }

        league_metadata = MetadataLeagueModel.query. \
            filter(MetadataLeagueModel.id == league_id). \
            filter(MetadataLeagueModel.status == 'ongoing'). \
            filter(MetadataLeagueModel.type == 'duel'). \
            order_by(MetadataLeagueModel.id.desc()). \
            first()
        if league_metadata is None:
            abort(404)

        history = LeagueDuelHistoryModel.query. \
            filter(LeagueDuelHistoryModel.league_id == league_id). \
            filter(LeagueDuelHistoryModel.user_id1 == request_user.id). \
            filter(LeagueDuelHistoryModel.state == 'start'). \
            first()
        if history is None:
            abort(404)

        if history.state != 'start':
            return {
                'success': False,
                'message': 'duel is not started'
            }

        history.state = request.args['result']

        # 누적 리그 시작에 추가
        accrue_user_achievement_value(request_user, 'league_try', 1)

        opponent_property = LeagueUserPropertyModel.query. \
            filter(LeagueUserPropertyModel.league_id == league_id). \
            filter(LeagueUserPropertyModel.user_id == history.user_id2). \
            first()

        # TODO : 과연 히스토리 숫자를 세는게 빠를까, column 을 늘리는게 빠를까?
        if history.state == 'win':
            # 누적 리그 승리 업적에 추가
            accrue_user_achievement_value(request_user, 'league_win', 1)
            league_user_property.win += 1
            opponent_property.lose += 1
        elif history.state == 'lose':
            opponent_property.win += 1
            league_user_property.lose += 1
        else:
            opponent_property.draw += 1
            league_user_property.draw += 1

        my_elo, opponent_elo = elo_calculation(league_user_property, opponent_property, history)

        league_user_property.elo = my_elo
        opponent_property.elo = opponent_elo

        league_user_property.ticket -= 1

        # 다음 상대 검색
        next_opponent = get_league_opponent(my_elo, league_id, request_user)
        if next_opponent is None:
            abort(500)

        new_history = LeagueDuelHistoryModel(league_id=league_id,
                                             user_id1=request_user.id,
                                             user_id2=next_opponent.user_id,
                                             state='ready')
        db.session.add(new_history)

        db.session.commit()

        return {
            'success': True,
        }

"""
    elo 시스템 적용
    R'a = rA + K * (sA-Ea)

    rA  : 플레이어의 현재 점수
    R'a : 승부 후 계산되는 점수
    Ea  : A 플레이어가 승리할 기대값
    Eb  : B 플레이어가 승리할 기대값
    sA  : A의 승패에 대한 점수 (승리시 1, 무승부 시 0.5, 패배 시 0)
    Ea: 1/(1+10^((rB-rA)/400))
    Eb: 1/(1+10^((rB-rA)/400))
    Ea + Eb = 1
"""


def elo_calculation(user, opponent, history):
    if history.state == 'win':
        sA = 1
        sB = 0
    elif history.state == 'lose':
        sA = 0
        sB = 1
    else:
        sA = 0.5
        sB = 0.5

    kA = 0
    if user.win + user.lose + user.draw < 30:
        kA = 25
    elif user.elo < 2400:
        kA = 15
    elif user.elo >= 2400:
        kA = 10

    kB = 0
    if opponent.win + opponent.lose + opponent.draw < 30:
        kB = 25
    elif opponent.elo < 2400:
        kB = 15
    elif opponent.elo >= 2400:
        kB = 10

    rA = user.elo
    rB = opponent.elo

    Ea = 1 / (1 + pow(10, (rB-rA)/400))
    Eb = 1 / (1 + pow(10, (rA-rB)/400))

    a_result = round(rA + kA * (sA - Ea))
    b_result = round(rB + kB * (sB - Eb))

    return a_result, b_result
