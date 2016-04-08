from app import get_constant_value, CONSTANTS_KEY_CLASS_BASIC_WEAPON_ID, CONSTANTS_KEY_CLASS_BASIC_ACCESSORY_ID
from app.util.give_item_equipment import give_item_equipment
from app.models.equipment import EquipmentModel
from app.models.metadata.hero import MetadataHeroModel

"""
    # UTIL : 영웅 기본 장비 제공
    # DESCRIPTION
        # 해당하는 영웅의 기본 장비 제공 (constant 테이블에서 가져옴)

"""


def give_hero_basic_equipment(request_user, hero):
    hero_metadata = MetadataHeroModel.query.\
        filter(MetadataHeroModel.id == hero.hero_metadata_id).\
        first()

    basic_hero_weapon_id = get_constant_value(CONSTANTS_KEY_CLASS_BASIC_WEAPON_ID, hero_metadata.hero_class)
    basic_hero_accessory_id = get_constant_value(CONSTANTS_KEY_CLASS_BASIC_ACCESSORY_ID, hero_metadata.hero_class)
    weapon = give_item_equipment(request_user, basic_hero_weapon_id)
    accessory = give_item_equipment(request_user, basic_hero_accessory_id)

    basic_hero_weapon = EquipmentModel.query.\
        filter(EquipmentModel.id == weapon['id']).\
        first()
    basic_hero_accessory = EquipmentModel.query. \
        filter(EquipmentModel.id == accessory['id']).\
        first()

    hero.equipment_id_weapon = basic_hero_weapon.id
    hero.equipment_id_accessory = basic_hero_accessory.id
    basic_hero_weapon.hero_id = hero.id
    basic_hero_accessory.hero_id = hero.id
    weapon['hero_id'] = hero.id
    accessory['hero_id'] = hero.id

    return {
        'weapon': weapon,
        'accessory': accessory,
    }
