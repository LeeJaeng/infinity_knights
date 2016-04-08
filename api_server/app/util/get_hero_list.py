from app.models.hero import HeroModel
from app import db

"""
    # UTIL : 영웅 리스트 반환
    # DESCRIPTION
        # 해당 유저의 영웅 리스트 반환

"""


def get_hero_list(request_user_id):
    heroes = HeroModel.query.\
        filter(HeroModel.user_id == request_user_id).\
        order_by(HeroModel.hero_metadata_id).\
        all()

    return heroes
