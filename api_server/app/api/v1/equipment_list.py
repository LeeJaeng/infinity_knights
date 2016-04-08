from app import api_root, db, access_token_required
from app.util.return_generator import get_equipment_return
from app.util.get_equipment_list import get_equipment_list
from flask.ext.restful import Resource

"""
    # API : 장비 리스트 조회
    # DESCRIPTION
        # 유저가 소유한 모든 장비 정보 반환

"""


@api_root.resource('/v1/equipments')
class EquipmentList(Resource):

    @access_token_required
    def get(self, request_user):

        equipments = get_equipment_list(request_user.id)

        result = []

        if equipments is None:
            return {
                'success': True,
                'result': result
            }

        for equipment in equipments:
            result.append(get_equipment_return(equipment.id))

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
