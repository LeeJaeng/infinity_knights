from app.models.equipment_option import EquipmentOptionModel
from app.models.equipment import EquipmentModel


def get_equipment_return(equipment_id):
    equipment = EquipmentModel.query.\
        filter(EquipmentModel.id == equipment_id).\
        first()

    equipment_options = EquipmentOptionModel.query.\
        filter(EquipmentOptionModel.equipment_id == equipment.id).\
        order_by(EquipmentOptionModel.id.asc()).\
        all()

    option_id_list = []
    option_value_list = []
    for option in equipment_options:
        option_id_list.append(option.option_metadata_id)
        option_value_list.append(option.value)

    result = {
        'id': equipment.id,
        'hero_id': equipment.hero_id,
        'equipment_metadata_id': equipment.equipment_metadata_id,
        'enchant_level': equipment.enchant_level,
        'enchant_level_limit': equipment.enchant_level_limit,
        'curr_breakthrough_point': equipment.curr_breakthrough_point,
        'next_breakthrough_cost': equipment.next_breakthrough_cost,
        'equipment_option_id_list': option_id_list,
        'equipment_option_value_list': option_value_list,
     }

    return result

