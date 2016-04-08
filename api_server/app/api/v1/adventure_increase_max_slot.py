from app import api_root, db, access_token_required
from app import get_constant_value, CONSTANTS_KEY_ADVENTURE_MAX_SLOT
from flask.ext.restful import Resource, request, abort
from app.models.adventure import AdventureModel
from app.util.get_adventure_random_list import get_adventure_random_one

"""
    # API : 모험 최대 슬롯 증가
    # DESCRIPTION
        # 과금 재화인 gem을 이용하여서 모험 최대 슬롯을 증가시킴

"""


@api_root.resource('/v1/adventures/increase-max-slot')
class AdventureIncreaseMaxSlot(Resource):
    @access_token_required
    def get(self, request_user):
        if 'cost' not in request.args:
            abort(400)
        cost = int(request.args['cost'])

        if cost > request_user.gem:
            return {
                'success': False,
                'message': 'not enough gem'
            }

        if request_user.adventure_slot >= get_constant_value(CONSTANTS_KEY_ADVENTURE_MAX_SLOT):
            return {
                'success': False,
                'message': 'already Max slot'
            }

        request_user.gem -= cost
        request_user.adventure_slot += 1

        adventure_list = AdventureModel.query.\
            filter(AdventureModel.user_id == request_user.id).\
            filter(AdventureModel.visible == False).\
            all()

        adventure = get_adventure_random_one(adventure_list, request_user)
        adventure.visible = True
        result = {
            'id': adventure.id,
            'adventure_metadata_id': adventure.adventure_metadata_id,
            'visible': adventure.visible,
            'execution_count': adventure.execution_count
        }

        db.session.commit()

        return {
            'success': True,
            'adventure_slot': request_user.adventure_slot,
            'gem': request_user.gem,
            'result': result
        }
