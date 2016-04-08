from app import api_root, db, access_token_required, get_constant_value, \
    CONSTANTS_KEY_DUNGEON_MAX_TICKET, CONSTANTS_KEY_DUNGEON_MAX_TICKET_INCREASE_PRICE, \
    CONSTANTS_KEY_DUNGEON_TICKET_INCREASE_INTERVAL_IN_SECONDS
from app.models.dungeon_activity import DungeonActivityModel
from flask.ext.restful import Resource, request
"""
    # API : 던전 티켓 증가
    # DESCRIPTION
        # 던전 티켓 충전

"""


@api_root.resource('/v1/infinity-dungeon/increase-ticket')
class InfinityDungeonIncreaseTicket(Resource):
    @access_token_required
    def get(self, request_user):
        ticket_count = int(request.args['ticket_count'])

        activity = DungeonActivityModel.query. \
            filter(DungeonActivityModel.user_id == request_user.id). \
            first()

        if activity.ticket + ticket_count > activity.max_ticket:
            return {
                'success': False,
                'message': 'overflowing max ticket'
            }

        activity.ticket += ticket_count
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'ticket': activity.ticket
        }
