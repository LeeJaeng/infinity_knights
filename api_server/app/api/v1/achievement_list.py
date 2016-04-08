from app import db, api_root, access_token_required
from app.models.user_achievement import UserAchievementModel
from flask.ext.restful import Resource

"""
    # API : 유저 업적 리스트
    # DESCRIPTION
        # 현재 사용자가 달성해 나가고 있는 유저 업적 리스트를 반환한다.

"""


@api_root.resource('/v1/achievements')
class AchievementList(Resource):
    @access_token_required
    def get(self, request_user):
        user_achievement = UserAchievementModel.query.\
            filter(UserAchievementModel.user_id == request_user.id).\
            first()

        result = user_achievement.property_to_dict()

        return {
            'success': True,
            'result': result
        }
