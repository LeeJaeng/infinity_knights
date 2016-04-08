from app import api_root, access_token_required, db
from app.models.league_duel_history import LeagueDuelHistoryModel
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.metadata.league import MetadataLeagueModel
from app.util.league import get_league_opponent
from app.util.league import get_league_opponent_info
from flask.ext.restful import Resource, abort

"""
    # API : 리그 결투 상대 변경
    # DESCRIPTION
        # 과금 재화인 gem을 이용하여 리그 결투 상대 변경
        # 현재 history를 가져와서 찾은 다음 상대 정보로 변경
        # TODO: elo 적용

"""


@api_root.resource('/v1/leagues/duels/<int:league_id>/opponent-change')
class LeagueDuelOpponentChange(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        league_metadata = MetadataLeagueModel.query. \
            filter(MetadataLeagueModel.id == league_id). \
            filter(MetadataLeagueModel.status == 'ongoing'). \
            filter(MetadataLeagueModel.type == 'duel'). \
            order_by(MetadataLeagueModel.id.desc()). \
            first()
        if league_metadata is None:
            abort(404)

        if request_user.gem < league_metadata.change_opponent_price:
            return {
                'success': False,
                'message': 'not enough gem'
            }

        history = LeagueDuelHistoryModel.query. \
            filter(LeagueDuelHistoryModel.league_id == league_id). \
            filter(LeagueDuelHistoryModel.user_id1 == request_user.id). \
            filter(LeagueDuelHistoryModel.state == 'ready'). \
            first()
        if history is None:
            abort(404)

        my_league_property = LeagueUserPropertyModel.query.\
            with_entities(LeagueUserPropertyModel.elo).\
            filter(LeagueUserPropertyModel.user_id == request_user.id).\
            filter(LeagueUserPropertyModel.league_id == league_id).\
            first()

        opponent = get_league_opponent(my_league_property.elo, league_id, request_user)
        if opponent is None:
            abort(500)

        history.user_id2 = opponent.user_id

        opponent_property_dict = get_league_opponent_info(league_id, history.user_id2)

        request_user.gem -= league_metadata.change_opponent_price

        db.session.commit()

        return {
            'success': True,
            'gem': request_user.gem,
            'opponent_property': opponent_property_dict
        }
