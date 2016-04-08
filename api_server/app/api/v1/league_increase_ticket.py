from app import api_root, db, access_token_required
from app.models.league_user_property import LeagueUserPropertyModel
from flask.ext.restful import Resource, abort, request

"""
    # API : 리그 티켓 증가
    # DESCRIPTION
        # 리그 티켓 충전

"""


@api_root.resource('/v1/leagues/<int:league_id>/increase-ticket')
class LeagueIncreaseTicket(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        ticket_count = int(request.args['ticket_count'])

        league_property = LeagueUserPropertyModel.query.\
            filter(LeagueUserPropertyModel.user_id == request_user.id).\
            filter(LeagueUserPropertyModel.league_id == league_id).\
            first()

        if league_property.ticket + ticket_count > league_property.max_ticket:
            return {
                'success': False,
                'message': 'overflowing max ticket'
            }

        league_property.ticket += ticket_count
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'ticket': league_property.ticket
        }
