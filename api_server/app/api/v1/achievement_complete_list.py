from app import db, api_root, access_token_required
from app.models.achievement import AchievementModel
from flask.ext.restful import Resource

"""
    # API : 업적 완료 리스트
    # DESCRIPTION
        # User가 업적을 달성해 보상을 수령한 id 리스트 반환
"""


@api_root.resource('/v1/achievements/complete')
class AchievementCompleteList(Resource):
    @access_token_required
    def get(self, request_user):
        result = []
        achievements = AchievementModel.query.\
            with_entities(AchievementModel.achievement_metadata_id).\
            filter(AchievementModel.user_id == request_user.id).\
            all()

        if achievements is None:
            return {
                'success': True,
                'result': result
            }

        for achievement in achievements:
            result.append(achievement.achievement_metadata_id)

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
