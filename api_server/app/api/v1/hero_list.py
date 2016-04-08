from app import api_root, db, access_token_required
from app.models.hero import HeroModel
from app.util.get_hero_list import get_hero_list
from flask.ext.restful import Resource

"""
    # API : 영웅 리스트 조회
    # DESCRIPTION
        # 유저의 모든 영웅 리스트 반환
        # 계약된(visible=True)영웅 계약되지 않은(visible=False)영웅 모두 반환

"""


@api_root.resource('/v1/heroes')
class HeroList(Resource):

    @access_token_required
    def get(self, request_user):

        heroes = get_hero_list(request_user.id)

        result = []
        for hero in heroes:
            result.append({
                'id': hero.id,
                'hero_metadata_id': hero.hero_metadata_id,
                'enchant_level': hero.enchant_level,
                'soul_stone': hero.soul_stone,
                'skill_1_level': hero.skill_1_level,
                'skill_2_level': hero.skill_2_level,
                'skill_3_level': hero.skill_3_level,
                'equipment_id_weapon': hero.equipment_id_weapon,
                'equipment_id_accessory': hero.equipment_id_accessory,
                'visible': hero.visible
            })

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
