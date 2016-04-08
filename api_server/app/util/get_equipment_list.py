from app.models.equipment import EquipmentModel
from app import db

"""
    # UTIL : 장비 리스트 반환
    # DESCRIPTION
        # 해당 유저의 장비 리스트 반환

"""


def get_equipment_list(request_user_id):
    equipments = EquipmentModel.query.\
        filter(EquipmentModel.user_id == request_user_id).\
        order_by(EquipmentModel.equipment_metadata_id).\
        all()

    return equipments
