from app import api_root, db, access_token_required, \
    get_constant_value, CONSTANTS_KEY_HERO_MAX_GRADE, CONSTANTS_KEY_HERO_PROMOTE_PRICE
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from flask import abort
from flask.ext.restful import Resource

"""
    # API : 영웅 승급
    # DESCRIPTION
        # 해당 영웅의 성(Star)이 올라감
        # hero 모델의 metadata_id가 바뀌는 것
        # 영혼석이 모자라면 종족 영혼석 사용

"""


@api_root.resource('/v1/heroes/<int:hero_id>/promote')
class HeroPromote(Resource):

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
                'message': 'hero is not opened yet '
            }

        metadata_hero = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id == hero.hero_metadata_id).\
            first()
        if metadata_hero is None:
            abort(404)

        if metadata_hero.grade == get_constant_value(CONSTANTS_KEY_HERO_MAX_GRADE):
            return {
                'success': False,
                'message': 'already max grade'
            }

        group = metadata_hero.group
        group_soul_stone = getattr(request_user, 'group_soul_stone_{}'.format(group))
        promote_price = get_constant_value(CONSTANTS_KEY_HERO_PROMOTE_PRICE, metadata_hero.grade)

        if promote_price > group_soul_stone + hero.soul_stone:
            return {
                'success': False,
                'message': 'not enough cost (soul_stone + group_soul_stone)'
            }

        metadata_upgrade_hero = MetadataHeroModel.query.\
            filter(MetadataHeroModel.name == metadata_hero.name).\
            filter(MetadataHeroModel.grade == metadata_hero.grade+1). \
            filter(MetadataHeroModel.is_evolve == metadata_hero.is_evolve).\
            first()

        hero.hero_metadata_id = metadata_upgrade_hero.id

        hero.soul_stone -= promote_price

        # using group_soul_stone for payment
        if hero.soul_stone < 0:
            setattr(request_user, 'group_soul_stone_{}'.format(group),
                    hero.soul_stone + group_soul_stone)
            hero.soul_stone = 0

        if metadata_upgrade_hero.grade == get_constant_value(CONSTANTS_KEY_HERO_MAX_GRADE):
            curr_g_soul_stone = getattr(request_user, 'group_soul_stone_{}'.format(group))
            setattr(request_user, 'group_soul_stone_{}'.format(group), curr_g_soul_stone + hero.soul_stone)
            hero.soul_stone = 0

        db.session.commit()

        return {
            'success': True,
            'hero_id': hero_id,
            'hero_metadata_id': metadata_upgrade_hero.id,
            'hero_grade': metadata_upgrade_hero.grade,
            'soul_stone': hero.soul_stone,
            'group_soul_stone_{}'.format(group): getattr(request_user, 'group_soul_stone_{}'.format(group))
        }
