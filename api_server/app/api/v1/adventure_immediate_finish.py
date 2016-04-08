from app import api_root, db, access_token_required
from app import get_constant_value, CONSTANTS_KEY_ADVENTURE_MAX_DISPATCH_NUM
from app.models.adventure import AdventureModel
from app.models.metadata.adventure import MetadataAdventureModel
from app.models.adventure_history import AdventureHistoryModel
from app.util.get_adventure_result import get_adventure_result
from app.util.set_user_achievement_value import accrue_user_achievement_value
from flask.ext.restful import Resource, request, abort

"""
    # API : 모험 즉시 완료
    # DESCRIPTION
        # 과금 재화인 gem을 이용하여 모험을 즉시 완료 시킴
        # adventure_get_reward.py와 같음

"""


@api_root.resource('/v1/adventures/immediate-finish')
class AdventureImmediateFinish(Resource):
    @access_token_required
    def get(self, request_user):
        if 'cost' not in request.args:
            abort(400)
        if 'adventure_id' not in request.args:
            abort(400)

        cost = int(request.args['cost'])
        adventure_id = int(request.args['adventure_id'])

        if request_user.gem < cost:
            return{
                'success': False,
                'message': 'Not enough gem'
            }

        adventure = AdventureModel.query.\
            filter(AdventureModel.id == adventure_id).\
            first()
        if adventure is None:
            abort(400)

        if not adventure.is_start:
            return{
                'success': False,
                'message': 'This adventure is not started'
            }

        metadata_adventure = MetadataAdventureModel.query. \
            filter(MetadataAdventureModel.id == adventure.adventure_metadata_id). \
            first()
        if metadata_adventure is None:
            abort(400)

        # 결과 확인 및 보상
        result = get_adventure_result(request_user, adventure, metadata_adventure)
        adventure.is_start = False
        adventure.visible = False
        request_user.gem -= cost

        # 모험 성공 시 , 업적에 추가, 모험 맥스레벨 증가
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

        # 모험에 참여한 영웅 복귀
        for i in range(0, get_constant_value(CONSTANTS_KEY_ADVENTURE_MAX_DISPATCH_NUM)):
            setattr(adventure, 'hero_{}_id'.format(i), None)
        db.session.commit()

        return {
            'success': True,
            'complete': result[0],
            'final_reward': result[1],
            'main_reward': result[2],
            'additional_reward': result[3],
            'gem': request_user.gem,
            'max_level': adventure.max_level
        }
