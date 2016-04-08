from app import api_root, db, access_token_required
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.metadata.league import MetadataLeagueModel
from app.worker.tasks.league_ticket import increase_league_ticket
from flask.ext.restful import Resource, abort

"""
    # API : 리그 최대 티켓 증가
    # DESCRIPTION
        # 과금 재화인 gem을 이용하여 최대 티켓량 증가
        # 티켓 증가시키는 비동기 함수 실행

"""


@api_root.resource('/v1/leagues/<int:league_id>/increase-max-ticket')
class LeagueIncreaseMaxTicket(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        league_metadata = MetadataLeagueModel.query. \
            filter(MetadataLeagueModel.id == league_id). \
            first()
        if league_metadata is None:
            abort(404)

        user_property = LeagueUserPropertyModel.query. \
            filter(LeagueUserPropertyModel.league_id == league_id). \
            filter(LeagueUserPropertyModel.user_id == request_user.id). \
            first()
        if user_property is None:
            abort(404)

        if user_property.max_ticket >= league_metadata.end_max_ticket:
            return {
                'success': False,
                'message': 'already ticket slot is full stack'
            }

        if request_user.gem < league_metadata.increase_max_ticket_price:
            return {
                'success': False,
                'message': 'not enough gem'
            }

        user_property.max_ticket += 1
        request_user.gem -= league_metadata.increase_max_ticket_price
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'max_ticket': user_property.max_ticket,
            'gem': request_user.gem
        }
