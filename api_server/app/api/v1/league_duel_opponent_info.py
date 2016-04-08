from app import api_root, access_token_required, db
from app.models.league_duel_history import LeagueDuelHistoryModel
from app.models.league_user_property import LeagueUserPropertyModel
from app.util.league import get_league_opponent_info
from app.util.league import get_league_opponent
from flask.ext.restful import Resource, abort

"""
    # API : 리그 결투 상대 정보
    # DESCRIPTION
        # 내 상대 정보 열람

"""


@api_root.resource('/v1/leagues/duels/<int:league_id>/opponent-info')
class LeagueDuelOpponentInfo(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        history = LeagueDuelHistoryModel.query. \
            filter(LeagueDuelHistoryModel.league_id == league_id). \
            filter(LeagueDuelHistoryModel.user_id1 == request_user.id). \
            filter(LeagueDuelHistoryModel.state == 'ready'). \
            first()
        # 현재 상대가 없는 경우
        my_property = LeagueUserPropertyModel.query. \
            filter(LeagueUserPropertyModel.league_id == league_id). \
            filter(LeagueUserPropertyModel.user_id == request_user.id). \
            first()

        if history is None:
            opponent_property = get_league_opponent(my_property.elo, league_id, request_user)
            if opponent_property:
                history = LeagueDuelHistoryModel(league_id=league_id,
                                                 user_id1=request_user.id,
                                                 user_id2=opponent_property.user_id,
                                                 state='ready')
                db.session.add(history)

        # 상대방 정보
        opponent_property_dict = None
        if history:
            opponent_property_dict = get_league_opponent_info(league_id, history.user_id2)

        # 내 정보
        my_property_dict = dict()
        my_property_dict['nickname'] = request_user.nickname
        my_property_dict['elo'] = my_property.elo
        my_property_dict['win'] = my_property.win
        my_property_dict['lose'] = my_property.lose
        my_property_dict['draw'] = my_property.draw

        my_rank, opponent_rank = get_rank_by_id(league_id, history.user_id1, history.user_id2)
        opponent_property_dict['rank'] = opponent_rank
        my_property_dict['rank'] = my_rank

        db.session.commit()

        # TODO : show more information about heroes
        # TODO : marshalling
        return {
            'success': True,
            'my_property': my_property_dict,
            'opponent_property': opponent_property_dict,
            'history_id': history.id
        }


def get_rank_by_id(league_id, user_id1, user_id2):
    properties = LeagueUserPropertyModel.query.\
        with_entities(LeagueUserPropertyModel.elo, LeagueUserPropertyModel.user_id).\
        filter(LeagueUserPropertyModel.league_id == league_id).\
        order_by(LeagueUserPropertyModel.elo.desc()).\
        all()

    user1_rank, user2_rank, rank, count = 1, 1, 1, 0
    token = 0
    prev_elo = 0

    for data in properties:
        count += 1
        if count != 1:
            if prev_elo != data.elo:
                rank = count
        if data.user_id == user_id1:
            user1_rank = rank
            token += 1
        if data.user_id == user_id2:
            user2_rank = rank
            token += 1
        prev_elo = data.elo

        if token == 2:
            return user1_rank, user2_rank
