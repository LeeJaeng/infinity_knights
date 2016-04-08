import math
from app import api_root, db, access_token_required
from app.models.equipment import EquipmentModel
from app.models.metadata.equipment import MetadataEquipmentModel
from flask import abort
from flask.ext.restful import Resource

"""
    # API : 장비 강화
    # DESCRIPTION
        # 계산 식을 이용하여서 강화 가격 및 능력 계산 후
        # 장비 강화

"""


@api_root.resource('/v1/equipments/<int:equipment_id>/enchant')
class EquipmentEnchant(Resource):
    @access_token_required
    def get(self, request_user, equipment_id):
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

        # current enchant level >= limit enchant level
        if equipment.enchant_level >= equipment.enchant_level_limit:
            return {
                'success': False,
                'message': 'enchant-level limit'
            }

        # price CALCULATION
        # enchant_price = (basic_enchant_price) * (price_rate ^ current_level)
        enchant_price = math.floor(metadata_equipment.base_enchant_cost * pow(
            metadata_equipment.enchant_cost_rate, equipment.enchant_level))
        if request_user.rune_stone < enchant_price:
            return {
                'success': False,
                'message': 'not enough rune'
            }

        # ability CALCULATION
        enchant_ability = metadata_equipment.basic_ability_value * pow(
            metadata_equipment.enchant_ability_rate, equipment.enchant_level+1)

        # SUCCESS RESULT
        # 1. level + 1
        # 2. payment
        # 3. applying ability
        equipment.enchant_level += 1
        request_user.rune_stone -= enchant_price
        equipment.basic_ability = enchant_ability

        db.session.commit()

        return {
            'success': True,
            'equipment_id': equipment_id,
            'enchant_level': equipment.enchant_level,
            'enchant_ability': enchant_ability,
            'rune_stone': request_user.rune_stone
        }
