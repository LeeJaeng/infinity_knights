from app import api_root, db, access_token_required
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from flask import abort
from flask.ext.restful import Resource

"""
    # API : 영웅 스킬 업그레이드
    # DESCRIPTION
        # 해당 번호 스킬 업그레이드

"""


@api_root.resource('/v1/heroes/<int:hero_id>/skill/<int:skill_number>/upgrade')
class HeroSkillUpgrade(Resource):
    @access_token_required
    def get(self, request_user, hero_id, skill_number):
        hero = HeroModel.query.\
            filter(HeroModel.id == hero_id).\
            first()
        if hero is None:
            abort(404)
        if hero.user_id != request_user.id:
            abort(400)

        metadata_hero = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id == hero.hero_metadata_id).\
            first()
        if metadata_hero is None:
            abort(404)

        target_skill_level = getattr(hero, 'skill_{}_level'.format(skill_number))
        upgrade_price = round(metadata_hero.base_skill_upgrade_cost *
                              pow(metadata_hero.skill_upgrade_cost_increase_rate, target_skill_level))

        if request_user.rune_stone < upgrade_price:
            return {
                'success': False,
                'message': 'not enough rune'
            }

        request_user.rune_stone -= upgrade_price
        setattr(hero, 'skill_{}_level'.format(skill_number), target_skill_level+1)
        db.session.commit()

        return {
            'success': True,
            'hero_id': hero_id,
            'skill_number': skill_number,
            'skill_level': target_skill_level+1,
            'rune_stone': request_user.rune_stone
        }
