from app import api_root, db, access_token_required, get_constant_value, \
    CONSTANTS_KEY_DUNGEON_TICKET_INCREASE_INTERVAL_IN_SECONDS
from app.models.dungeon_activity import DungeonActivityModel
from app.worker.tasks.dungeon_ticket import increase_dungeon_ticket
from flask.ext.restful import Resource
from datetime import datetime, timedelta

"""
    # API : 던전 입장
    # DESCRIPTION
        # 티켓을 감소시키고 worker를 비동기적으로 실행
        # 티켓 증가 시간이 지나면 티켓 증가

"""


@api_root.resource('/v1/infinity-dungeon/enter')
class InfinityDungeonEnter(Resource):
    @access_token_required
    def get(self, request_user):
        activity = DungeonActivityModel.query. \
            filter(DungeonActivityModel.user_id == request_user.id). \
            first()

        # Time check해서 updated date가 1일 보다 더 전이면 초기화 시킴
        time_gap = timedelta(hours=request_user.time_gap)
        last_updated_date = activity.updated_date + time_gap
        curr_date = datetime.utcnow() + time_gap
        day_diff = (curr_date.date() - last_updated_date.date()).days

        if day_diff >= 1:
            activity.step = 1
            activity.enter = 0
            activity.achievement_list = []

        activity.is_start = True

        if activity.ticket <= 0:
            return {
                'success': False,
                'message': 'not enough ticket'
            }

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'step': activity.step,
        }
