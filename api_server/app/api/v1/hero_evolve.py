from app import api_root, db, access_token_required, get_constant_value, CONSTANTS_KEY_EVOLVE_GEM_PRICE
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from flask import abort
from flask.ext.restful import Resource

"""
    # API : 영웅 각성
    # DESCRIPTION
        # 영웅이 각성한다는 것은 hero table 해당 영웅의 metadata id가 바뀌는 것

"""


@api_root.resource('/v1/heroes/<int:hero_id>/evolve')
class HeroEvolve(Resource):
    @access_token_required
    def get(self, request_user, hero_id):
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
                'message': 'hero is not opened yet'
            }

        hero_metadata = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id == hero.hero_metadata_id).\
            first()
        if hero_metadata is None:
            abort(404)

        # 이미 각성상태인지 확인
        if hero_metadata.is_evolve is True:
            return {
                'success': False,
                'message': 'Already evolved'
            }

        evolve_price = get_constant_value(CONSTANTS_KEY_EVOLVE_GEM_PRICE)
        # user gem 확인
        if request_user.gem < evolve_price:
            return {
                'success': False,
                'message': 'not enough gem'
            }
        request_user.gem -= evolve_price

        # NEW : Same name, Same grade, evolved
        new_hero_metadata = MetadataHeroModel.query.\
            filter(MetadataHeroModel.name == hero_metadata.name).\
            filter(MetadataHeroModel.grade == hero_metadata.grade). \
            filter(MetadataHeroModel.is_evolve).\
            first()
        if new_hero_metadata is None:
            abort(404)

        hero.hero_metadata_id = new_hero_metadata.id
        db.session.commit()

        return {
            'success': True,
            'hero_id': hero_id,
            'hero_metadata_id': new_hero_metadata.id,
            'gem': request_user.gem
        }
