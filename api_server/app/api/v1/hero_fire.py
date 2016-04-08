from app import api_root, db, access_token_required
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from flask import abort
from flask.ext.restful import Resource

"""
    # API : 영웅 해고
    # DESCRIPTION
        # 해당 영웅 해고 (visible=False)

"""


@api_root.resource('/v1/heroes/<int:hero_id>/fire')
class HeroFire(Resource):
    @access_token_required
    def get(self, request_user, hero_id):
        # find hero with id (from argument)
        hero = HeroModel.query.\
            filter(HeroModel.id == hero_id).\
            first()

        # if there is not hero
        if hero is None:
            abort(404)
        # this hero is not user's hero
        if hero.user_id != request_user.id:
            abort(404)

        if not hero.visible:
            return {
                'success': False,
                'message': 'You do not have this hero'
            }

        metadata_hero = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id == hero.hero_metadata_id).\
            first()
        if metadata_hero is None:
            abort(404)

        # find basic grade hero
        if not metadata_hero.is_basic_grade:
            basic_metadata_hero = MetadataHeroModel.query.\
                filter(MetadataHeroModel.name == metadata_hero.name).\
                filter(MetadataHeroModel.is_basic_grade). \
                first()
            hero.hero_metadata_id = basic_metadata_hero.id

        hero.visible = False
        hero.soul_stone = 0
        db.session.commit()

        return {
            'success': True,
            'hero_id': hero_id
        }
