from app import api_root, db, access_token_required, get_constant_value, \
    CONSTANTS_KEY_DUNGEON_MAX_TICKET, CONSTANTS_KEY_DUNGEON_MAX_TICKET_INCREASE_PRICE, \
    CONSTANTS_KEY_DUNGEON_TICKET_INCREASE_INTERVAL_IN_SECONDS
from app.models.dungeon_activity import DungeonActivityModel
from app.worker.tasks.dungeon_ticket import increase_dungeon_ticket
from flask.ext.restful import Resource

"""
    # API : 던전 최대 티켓량 증가
    # DESCRIPTION
        # 과금 재화 gem을 이용해서 던전 최대 티켓량 증가
        # 티켓 증가시키는 비동기 함수 실행

"""


@api_root.resource('/v1/infinity-dungeon/increase-max-ticket')
class InfinityDungeonIncreaseMaxTicket(Resource):
    @access_token_required
    def get(self, request_user):
        activity = DungeonActivityModel.query. \
            filter(DungeonActivityModel.user_id == request_user.id). \
            first()

        if activity.max_ticket >= get_constant_value(CONSTANTS_KEY_DUNGEON_MAX_TICKET):
            return {
                'success': False,
                'message': 'already ticket slot is full stack'
            }

        if request_user.gem < get_constant_value(CONSTANTS_KEY_DUNGEON_MAX_TICKET_INCREASE_PRICE):
            return {
                'success': False,
                'message': 'not enough gem'
            }

        request_user.gem -= get_constant_value(CONSTANTS_KEY_DUNGEON_MAX_TICKET_INCREASE_PRICE)
        activity.max_ticket += 1
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'max_ticket': activity.max_ticket,
            'gem': request_user.gem
        }
