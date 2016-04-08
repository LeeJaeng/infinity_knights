from app import api_root, db, access_token_required
from app.models.dungeon_activity import DungeonActivityModel
from app.models.metadata.dungeon_achievements import MetadataDungeonAchievementModel
from app.util.get_reward import get_reward
from flask.ext.restful import Resource, abort, request

"""
    # API : 던전 종료
    # DESCRIPTION
        # 전 스텝, 현재 스텝을 비교하여서 지급할 룬스톤 보상량 계산
        # 아직 받지 않은 보상인 경우 받도록 함
        # 누적 룬스톤 업적 추가

"""


@api_root.resource('/v1/infinity-dungeon/exit')
class InfinityDungeonExit(Resource):
    @access_token_required
    def get(self, request_user):
        if 'step' not in request.args:
            abort(400)

        activity = DungeonActivityModel.query. \
            filter(DungeonActivityModel.user_id == request_user.id). \
            first()

        if not activity.is_start:
            return {
                'success': False,
                'message': 'dungeon is not started'
            }

        curr_step = int(request.args['step'])

        activity.step = curr_step
        activity.enter += 1
        db.session.commit()

        achieved_metadata_id_list = []
        for data in activity.achievement_list:
            achieved_metadata_id_list.append(data)

        if len(achieved_metadata_id_list) != 0:
            left_achievements = MetadataDungeonAchievementModel.query. \
                filter(MetadataDungeonAchievementModel.id.notin_(achieved_metadata_id_list)). \
                all()
        else:
            left_achievements = MetadataDungeonAchievementModel.query. \
                all()

        reward = []
        for achievement in left_achievements:
            if achievement.value <= getattr(activity, str(achievement.type)):
                reward.append(get_reward(request_user, achievement.reward_name))
                achieved_metadata_id_list.append(achievement.id)

        # 입장 횟수 증가, 티켓 감소
        activity.ticket -= 1
        activity.is_start = False
        setattr(activity, 'achievement_list', achieved_metadata_id_list)
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'enter': activity.enter,
            'ticket': activity.ticket,
            'reward': reward
        }
