from app import api_root, db, access_token_required, get_constant_value, \
    CONSTANTS_KEY_DUNGEON_TICKET_PRICE
from app.models.dungeon_activity import DungeonActivityModel
from flask.ext.restful import Resource

"""
    # API : 무한 던전 티켓 구매
    # DESCRIPTION
        # 과금 재화인 gem을 이용해 무한던전 티켓 구매해서 바로 던전 입장

"""


@api_root.resource('/v1/infinity-dungeon/buy-ticket')
class InfinityDungeonBuyTicket(Resource):
    @access_token_required
    def get(self, request_user):
        activity = DungeonActivityModel.query. \
            filter(DungeonActivityModel.user_id == request_user.id). \
            first()

        if request_user.gem < get_constant_value(CONSTANTS_KEY_DUNGEON_TICKET_PRICE):
            return {
                'success': False,
                'message': 'not enough gem'
            }

        request_user.gem -= get_constant_value(CONSTANTS_KEY_DUNGEON_TICKET_PRICE)
        activity.enter += 1
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'step': activity.step,
            'enter': activity.enter,
            'gem': request_user.gem
        }
