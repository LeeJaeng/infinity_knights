from app import api_root, access_token_required, db
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.league_duel_history import LeagueDuelHistoryModel
from flask.ext.restful import Resource, abort

"""
    # API : 리그 결투 시작
    # DESCRIPTION
        # 정해진 상대와 리그전 시작
        # 누적 리그 시작 업적 추가

"""


@api_root.resource('/v1/leagues/duels/<int:league_id>/duel-start')
class LeagueDuelStart(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        league_user_property = LeagueUserPropertyModel.query. \
            with_entities(LeagueUserPropertyModel.ticket).\
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

        history = LeagueDuelHistoryModel.query.\
            filter(LeagueDuelHistoryModel.user_id1 == request_user.id).\
            filter(LeagueDuelHistoryModel.league_id == league_id).\
            first()

        history.state = 'start'
        db.session.commit()

        return {
            'success': True
        }
