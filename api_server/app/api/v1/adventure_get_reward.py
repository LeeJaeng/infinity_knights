from app import api_root, db, access_token_required
from app import get_constant_value, CONSTANTS_KEY_ADVENTURE_MAX_DISPATCH_NUM
from app.models.adventure import AdventureModel
from app.models.metadata.adventure import MetadataAdventureModel
from app.models.adventure_history import AdventureHistoryModel
from app.util.get_adventure_result import get_adventure_result
from app.util.set_user_achievement_value import accrue_user_achievement_value
from flask.ext.restful import Resource, request, abort
from datetime import datetime, timedelta

"""
    # API : 모험 보상 (끝)
    # DESCRIPTION
        # 모험이 끝난 후 성공했는지 아닌지 확인
        # 성공 시 해당하는 보상 제공
        # 모험이 끝나면 모험 히스토리 모델에 추가
        # 모험 성공 업적 추가

"""


@api_root.resource('/v1/adventures/get-reward')
class AdventureGetReward(Resource):
    @access_token_required
    def get(self, request_user):
        if 'adventure_id' not in request.args:
            abort(400)

        adventure_id = int(request.args['adventure_id'])

        adventure = AdventureModel.query.\
            filter(AdventureModel.id == adventure_id).\
            first()
        if adventure is None:
            abort(400)

        if not adventure.is_start:
            return {
                'success': False,
                'message': 'adventure is not started'
            }

        metadata_adventure = MetadataAdventureModel.query.\
            filter(MetadataAdventureModel.id == adventure.adventure_metadata_id).\
            first()
        if metadata_adventure is None:
            abort(400)

        # 시간 검증
        """
        curr_time = datetime.utcnow()
        time_gap = timedelta(minutes=metadata_adventure.run_duration)
        if curr_time - time_gap < adventure.updated_date:
            return {
                'success': False,
                'message': 'too fast ending'
            }
        """

        # 결과 확인 및 보상
        result = get_adventure_result(request_user, adventure, metadata_adventure)
        adventure.is_start = False
        adventure.visible = False

        # 모험 성공 시, 업적에 추가, 모험 레벨 증가
        if result[0]:
            if adventure.max_level == metadata_adventure.level:
                adventure.max_level += 1
            accrue_user_achievement_value(request_user, 'adventure_success', 1)

        # 히스토리 등록
        adventure_history = AdventureHistoryModel(
                user_id=request_user.id,
                adventure_metadata_id=metadata_adventure.id,
                hero_1_id=adventure.hero_1_id,
                hero_2_id=adventure.hero_2_id,
                hero_3_id=adventure.hero_3_id,
                is_complete=result[0]
        )
        db.session.add(adventure_history)

        # 모험에 참여한 영웅들을 복귀 시킴
        for i in range(1, get_constant_value(CONSTANTS_KEY_ADVENTURE_MAX_DISPATCH_NUM)):
            setattr(adventure, 'hero_{}_id'.format(i), None)
        db.session.commit()

        return {
            'success': True,
            'complete': result[0],
            'final_reward': result[1],
            'main_reward': result[2],
            'additional_reward': result[3],
            'max_level': adventure.max_level
        }
