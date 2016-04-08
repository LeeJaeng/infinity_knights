from app import api_root, db, access_token_required
from app.util.give_hero_basic_equipment import give_hero_basic_equipment
from app.util.return_generator import get_equipment_return
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from flask import abort
from flask.ext.restful import Resource

"""
    # API : 영웅 계약
    # DESCRIPTION
        # 영웅의 영혼석이 충분하다면 영웅 계약 가능
        # 기본 무기 지급

"""


@api_root.resource('/v1/heroes/<hero_id>/hire')
class HeroHire(Resource):
    @access_token_required
    def get(self, request_user, hero_id):

        hero = HeroModel.query.\
            filter(HeroModel.id == hero_id).\
            first()
        if hero is None:
            abort(404)

        metadata_hero = MetadataHeroModel.query.\
            with_entities(MetadataHeroModel.hire_cost).\
            filter(MetadataHeroModel.id == hero.hero_metadata_id).\
            first()

        if hero.visible:
            return {
                'success': False,
                'message': 'already hero is hired'
            }
        if hero.soul_stone < metadata_hero.hire_cost:
            return {
                'success': False,
                'message': 'not enough soul_stone'
            }

        # give default equipment
        give_hero_basic_equipment(request_user, hero)

        hero.visible = True
        hero.soul_stone -= metadata_hero.hire_cost
        db.session.commit()

        equipment = dict()
        equipment['weapon'] = get_equipment_return(hero.equipment_id_weapon)
        equipment['accessory'] = get_equipment_return(hero.equipment_id_accessory)

        # TODO : marshalling
        return {
            'success': True,
            'hero_id': hero.id,
            'soul_stone': hero.soul_stone,
            'equipment': equipment
        }
