import random
from decimal import Decimal
from app import db
from app.models.equipment import EquipmentModel
from app.models.equipment_option import EquipmentOptionModel
from app.models.metadata.equipment_option import MetadataEquipmentOptionModel
from app.models.metadata.equipment import MetadataEquipmentModel
from flask.ext.restful import abort


def get_random_value(min_value, max_value, base_unit):
    value = random.uniform(min_value, max_value)
    if base_unit == '1':
        value = round(value)
    elif base_unit == '0.1':
        value = round(value, 1)

    return value


def create_option(equipment_id, equipment_metadata_id):
    metadata_equipment_options = MetadataEquipmentOptionModel.query.\
        filter(MetadataEquipmentOptionModel.equipment_metadata_id == equipment_metadata_id).\
        all()
    if metadata_equipment_options is None or len(metadata_equipment_options) == 0:
        return None

    options = []
    for metadata_equipment_option in metadata_equipment_options:
        value = get_random_value(metadata_equipment_option.min_value,
                                 metadata_equipment_option.max_value,
                                 metadata_equipment_option.base_unit)
        new_equipment_option = EquipmentOptionModel(
            equipment_id=equipment_id,
            option_metadata_id=metadata_equipment_option.id,
            value=value
        )
        db.session.add(new_equipment_option)
        options.append(new_equipment_option)
    return options

"""
    # UTIL : 장비 주기
    # DESCRIPTION
        # 장비 메타아이디를 입력하여 호출하면 해당 장비 생성
        # 생성 전 옵션을 먼저 생성해야 함

"""


def give_item_equipment(request_user, target_metadata_id):
        metadata_equipment = MetadataEquipmentModel.query.\
            filter(MetadataEquipmentModel.id == target_metadata_id).\
            first()

        new_equipment = EquipmentModel(
            user_id=request_user.id,
            hero_id=None,
            equipment_metadata_id=target_metadata_id,
            basic_ability=metadata_equipment.basic_ability_value,
            next_breakthrough_cost=metadata_equipment.base_breakthrough_cost
        )
        db.session.add(new_equipment)
        # commit needed.

        options = create_option(new_equipment.id, new_equipment.equipment_metadata_id)
        db.session.commit()

        option_id_list = []
        option_value_list = []
        if options:
            for option in options:
                option_id_list.append(option.option_metadata_id)
                option_value_list.append(option.value)

        result = {
            'id': new_equipment.id,
            'hero_id': new_equipment.hero_id,
            'equipment_metadata_id': new_equipment.equipment_metadata_id,
            'enchant_level': new_equipment.enchant_level,
            'enchant_level_limit': new_equipment.enchant_level_limit,
            'curr_breakthrough_point': new_equipment.curr_breakthrough_point,
            'next_breakthrough_cost': new_equipment.next_breakthrough_cost,
            'equipment_option_id_list': option_id_list,
            'equipment_option_value_list': option_value_list,
        }

        return result

