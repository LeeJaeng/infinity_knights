from app import api_root, db, access_token_required
from app.models.hero import HeroModel
from app.models.equipment import EquipmentModel
from app.models.metadata.equipment import MetadataEquipmentModel
from flask import request, abort
from flask.ext.restful import Resource

"""
    # API : 영웅 무기 장착 및 해체
    # DESCRIPTION
        # 영웅 무기 장착 및 해체

"""


@api_root.resource('/v1/heroes/<int:hero_id>/equipments/weapon/put-on')
class HeroEquipmentWeaponPutOn(Resource):
    @access_token_required
    def get(self, request_user, hero_id):
        if 'equipment_id' not in request.args:
            abort(400)

        equipment_id = request.args['equipment_id']

        hero = HeroModel.query.\
            filter(HeroModel.id == hero_id).\
            first()
        if hero is None:
            abort(404)
        if hero.user_id != request_user.id:
            abort(400)

        equipment = EquipmentModel.query.\
            filter(EquipmentModel.id == equipment_id).\
            first()
        if equipment is None:
            abort(404)
        if equipment.hero_id is not None and equipment.hero_id != hero_id:
            abort(400)

        if hero.equipment_id_weapon is not None:
            prev_equipment = EquipmentModel.query.\
                filter(EquipmentModel.id == hero.equipment_id_weapon).\
                first()
            prev_equipment.hero_id = None
            hero.equipment_id_weapon = None

        equipment_metadata = MetadataEquipmentModel.query.\
            filter(MetadataEquipmentModel.id == equipment.equipment_metadata_id).\
            first()
        if equipment_metadata.type != 'weapon':
            abort(400)

        hero.equipment_id_weapon = equipment.id
        equipment.hero_id = hero.id
        db.session.commit()

        return {
            'success': True,
            'hero_id': hero_id,
            'equipment_id': int(equipment_id)
        }


@api_root.resource('/v1/heroes/<int:hero_id>/equipments/weapon/put-off')
class HeroEquipmentWeaponPutOff(Resource):
    @access_token_required
    def get(self, request_user, hero_id):
        hero = HeroModel.query.\
            filter(HeroModel.id == hero_id).\
            first()
        if hero is None:
            abort(404)

        if hero.user_id != request_user.id:
            abort(400)

        if hero.equipment_id_weapon is None:
            abort(400)

        equipment = EquipmentModel.query.\
            filter(EquipmentModel.id == hero.equipment_id_weapon).\
            first()
        if equipment is None:
            abort(404)
        if equipment.hero_id is not None and equipment.hero_id != hero_id:
            abort(400)

        hero.equipment_id_weapon = None
        equipment.hero_id = None
        db.session.commit()

        return {
            'success': True,
            'hero_id': hero_id,
        }
