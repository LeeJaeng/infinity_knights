from app import db
from app import get_constant_value, CONSTANTS_KEY_HERO_SOUL_STONE_BY_GRADE
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from app.util.give_hero_basic_equipment import give_hero_basic_equipment
from flask.ext.restful import abort


def give_item_hero(request_user, target_metadata_id):

    target_metadata = MetadataHeroModel.query.\
        filter(MetadataHeroModel.id == target_metadata_id).\
        first()

    subquery_find_metadata_id = db.session.query(MetadataHeroModel.id).\
        filter(MetadataHeroModel.name == target_metadata.name).\
        subquery()
    hero = HeroModel.query. \
        filter(HeroModel.user_id == request_user.id).\
        filter(HeroModel.hero_metadata_id.in_(subquery_find_metadata_id)).\
        first()
    if hero is None:
        abort(400)

    result = dict()
    if hero.visible:
        hero.soul_stone += \
            get_constant_value(CONSTANTS_KEY_HERO_SOUL_STONE_BY_GRADE, target_metadata.grade)
        result['soul_stone'] = hero.soul_stone
    else:
        hero.visible = True
        equipment = give_hero_basic_equipment(request_user, hero)
        result['equipment'] = equipment

    result['hero_id'] = hero.id

    return result
