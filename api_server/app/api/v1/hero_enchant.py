from app import api_root, db, access_token_required
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from app.util.set_user_achievement_value import update_user_achievement_value
from flask import abort, request
from flask.ext.restful import Resource

"""
    # API : 영웅 강화
    # DESCRIPTION
        # 강화 가격 계산하여서 반영
        # 최대 영웅 강화 레벨 업적 추가

"""


@api_root.resource('/v1/heroes/<int:hero_id>/enchant')
class HeroEnchant(Resource):
    @access_token_required
    def get(self, request_user, hero_id):
        count = 0
        if request.args['count'] is None:
            abort(400)

        count = int(request.args['count'])

        hero = HeroModel.query.\
            filter(HeroModel.id == hero_id).\
            first()
        if hero is None:
            abort(404)
        if hero.user_id != request_user.id:
            abort(400)

        if not hero.visible:
            return {
                'success': False,
                'message': 'this hero is not hired'
            }
        metadata_hero = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id == hero.hero_metadata_id).\
            first()
        if metadata_hero is None:
            abort(400)

        total_enchant_price = 0
        curr_enchant_level = hero.enchant_level
        for i in range(1, count + 1):
            enchant_price = (int)(metadata_hero.enchant_base_cost * pow(metadata_hero.enchant_cost_increase_rate, curr_enchant_level))
            total_enchant_price += enchant_price
            curr_enchant_level += 1

        if request_user.rune_stone < total_enchant_price:
            return {
                'success': False,
                'message': 'not enough rune'
            }

        request_user.rune_stone -= total_enchant_price
        hero.enchant_level += count
        # 최대 영웅 강화 업적에 추가
        update_user_achievement_value(request_user, 'max_hero_enchant', hero.enchant_level)
        db.session.commit()

        return {
            'success': True,
            'hero_id': hero_id,
            'rune_stone': request_user.rune_stone,
            'current_hero_enchant_level': hero.enchant_level
        }
