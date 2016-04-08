import datetime

from app import api_root, db, access_token_required, get_constant_value, CONSTANTS_KEY_MIN_TIME_CLEAR_ENEMY
from app.util.get_reward import get_reward
from app.models.metadata.stage import MetadataStageModel
from app.models.user_achievement import UserAchievementModel
from flask.ext.restful import Resource, abort, request

"""
    # API : 적 보스 처치
    # DESCRIPTION
        # 일반 stage에서 보스 몹들을 처치 했을 때 그에 알맞는 보상 제공
        # last_elite_killed_date를 이용한 Abusing 단속

"""


@api_root.resource('/v1/clear-enemy')
class ClearEnemy(Resource):
    @access_token_required
    def get(self, request_user):

        if request.args['world'] is None or request.args['stage'] is None:
            abort(404)

        world = int(request.args['world'])
        stage = int(request.args['stage'])

        curr_time = datetime.datetime.utcnow()
        diff_time = curr_time - request_user.last_elite_killed_date

        if diff_time.total_seconds() < get_constant_value(CONSTANTS_KEY_MIN_TIME_CLEAR_ENEMY):
            # maybe bug user
            # TODO : reporting?
            return {
                'success': False,
                'message': 'Too early clear'
            }

        stage_model = MetadataStageModel.query.\
            filter(MetadataStageModel.world == world).\
            filter(MetadataStageModel.stage == stage).\
            first()
        if stage_model is None:
            abort(400)

        result = []

        # 기본 보스 리워드
        if stage_model.boss_reward[0] != '':
            for reward in stage_model.boss_reward:
                result.append(get_reward(request_user, reward))

        # 최초로 주는 리워드
        if stage_model.first_reward[0] != '':
            for reward in stage_model.first_reward:
                user_achievement =UserAchievementModel.query.\
                    with_entities(UserAchievementModel.stage_world_1,
                                  UserAchievementModel.stage_world_2).\
                    filter(UserAchievementModel.user_id == request_user.id).\
                    first()
                if user_achievement is None:
                    abort(400)
                if world == 1:
                    if stage > user_achievement.stage_world_1:
                        result.append(get_reward(request_user, reward))
                elif world == 2:
                    if stage > user_achievement.stage_world_2:
                        result.append(get_reward(request_user, reward))

        request_user.last_elite_killed_date = datetime.datetime.utcnow()

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
