from app import api_root, db, access_token_required
from app import get_constant_value, CONSTANTS_KEY_BREAKTHROUGH_ENCHANT_LEVEL_INCREASE
from app.models.equipment import EquipmentModel
from app.models.metadata.equipment import MetadataEquipmentModel
from app.models.equipment_option import EquipmentOptionModel
from app.util.set_user_achievement_value import accrue_user_achievement_value
from flask import request, abort
from flask.ext.restful import Resource

"""
    # API : 장비 한계돌파
    # DESCRIPTION
        # 희생장비를 이용하여 해당 장비 최대 강화레벨 증가시킴
        # 희생장비는 이후 삭제
        # 누적 한계돌파 업적 추가

"""


@api_root.resource('/v1/equipments/<int:equipment_id>/breakthrough')
class EquipmentBreakthrough(Resource):
    @access_token_required
    def post(self, request_user, equipment_id):
        if 'victims' not in request.json:
            abort(400)

        victim_id_list = request.json['victims']
        # victim models
        victim_list = []

        total_victim_point = 0
        for victim_id in victim_id_list:
            victim_equipment = EquipmentModel.query. \
                filter(EquipmentModel.id == victim_id). \
                first()
            if victim_equipment is None:
                abort(404)
            if victim_equipment.user_id != request_user.id:
                abort(400)

            victim_list.append(victim_equipment)

            metadata_victim_equipment = MetadataEquipmentModel.query.\
                filter(MetadataEquipmentModel.id == victim_equipment.equipment_metadata_id).\
                first()
            if metadata_victim_equipment is None:
                abort(400)

            victim_point = metadata_victim_equipment.breakthrough_point + (metadata_victim_equipment.breakthrough_increase_by_enchant_level * victim_equipment.enchant_level)
            total_victim_point += victim_point

        equipment = EquipmentModel.query.\
            filter(EquipmentModel.id == equipment_id).\
            first()
        if equipment is None:
            abort(404)
        if equipment.user_id != request_user.id:
            abort(400)

        metadata_equipment = MetadataEquipmentModel.query.\
            filter(MetadataEquipmentModel.id == equipment.equipment_metadata_id).\
            first()
        if metadata_equipment is None:
            abort(400)


        equipment.curr_breakthrough_point += total_victim_point

        while equipment.curr_breakthrough_point >= equipment.next_breakthrough_cost:
            equipment.curr_breakthrough_point -= equipment.next_breakthrough_cost
            equipment.enchant_level_limit += get_constant_value(CONSTANTS_KEY_BREAKTHROUGH_ENCHANT_LEVEL_INCREASE)
            # 누적 한계돌파 업적에 누적 시킴
            accrue_user_achievement_value(request_user, 'accrue_breakthrough', 1)

            equipment.next_breakthrough_cost += metadata_equipment.breakthrough_cost_step
            if equipment.next_breakthrough_cost > metadata_equipment.breakthrough_cost_limit:
                equipment.next_breakthrough_cost = metadata_equipment.breakthrough_cost_limit

        # 지우기 전에 먼저 option 을 지워야 한다

        for victim in victim_list:
            equipment_options = EquipmentOptionModel.query. \
                filter(EquipmentOptionModel.equipment_id == victim.id). \
                all()
            if equipment_options:
                for option in equipment_options:
                    db.session.delete(option)
                    db.session.commit()
            db.session.delete(victim)

        db.session.commit()

        return {
            'success': True,
            'equipment_id': equipment_id,
            'curr_breakthrough_point': equipment.curr_breakthrough_point,
            'next_breakthrough_cost': equipment.next_breakthrough_cost,
            'enchant_level_limit': equipment.enchant_level_limit
        }
