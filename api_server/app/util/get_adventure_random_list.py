import random
from app.models.metadata.adventure import MetadataAdventureModel
from app.util.adventure_exeuction_refresh import adventure_execution_refresh
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from sqlalchemy import func, or_, and_


def weighted_random(li, choices, ratio_sum):
    r = random.uniform(0, ratio_sum)
    up = 0
    for i in range(0, len(choices)):
        if up + choices[i] >= r:
            return_value = li[i]
            li.remove(li[i])
            return return_value
        up += choices[i]


"""
    # UTIL : 모험 랜덤리스트 생성
    # DESCRIPTION
        # 모험 등장조건에 알맞는 모험이 최대 슬롯 수에 맞게 등장하도록 함
        # 등장 규칙
            # 각 모험 최대레벨에서 -3까
            # 등장 조건 영웅을 해당 유저가 가지고 있을 때

"""


def get_adventure_random_list(adventure_list, request_user):
    # hero name user has
    subquery_hero_metadata_id = HeroModel.query.\
        with_entities(HeroModel.hero_metadata_id).\
        filter(HeroModel.user_id == request_user.id).\
        filter(HeroModel.visible).\
        subquery()
    hero_names = MetadataHeroModel.query.\
        with_entities(MetadataHeroModel.name).\
        filter(MetadataHeroModel.id.in_(subquery_hero_metadata_id)).\
        all()

    result = []
    # for weighted random choice
    # 랜덤 뽑기를 위해서 넣을 것
    pick = []
    for adventure in adventure_list:
        # 이미 시작한 모험은 결과 리스트에 바로 넣는다
        if adventure.is_start:
            result.append(adventure)
            continue

        # 시작되지 않은 모험은 모험 등장 규칙에 맞게
        curr_adventure_name = MetadataAdventureModel.query.\
            with_entities(MetadataAdventureModel.name).\
            filter(MetadataAdventureModel.id == adventure.adventure_metadata_id). \
            subquery()
        target = MetadataAdventureModel.query. \
            filter(MetadataAdventureModel.name == curr_adventure_name). \
            filter(and_(MetadataAdventureModel.level <= adventure.max_level,
                        MetadataAdventureModel.level >= adventure.max_level-3)).\
            filter(or_(MetadataAdventureModel.hero_name_for_appear.in_(hero_names),
                       MetadataAdventureModel.hero_name_for_appear == None)).\
            order_by(func.random()).\
            first()
        if target:
            pick.append(target)
            adventure.adventure_metadata_id = target.id

    # Adventure 실행 횟수 리프레쉬(하루가 지났다면)
    adventure_execution_refresh(adventure_list, request_user)

    # 이미 스타트한 모험은 결과리스트에 있기 때문에 리스트의 나머지를 채워야 함
    remain_adventure_count = request_user.adventure_slot - len(result)

    # 모험 하루 수행 횟수를 다 만족한 모험은 리스트에 넣지 않는다.
    while remain_adventure_count != 0 and len(pick) != 0:
        choice = weighted_random(pick,
                                 [adventure.appear_rate for adventure in pick],
                                 sum(adventure.appear_rate for adventure in pick))
        for adventure in adventure_list:
            if adventure.adventure_metadata_id == choice.id:
                if adventure.execution_count < choice.execution_limit:
                    result.append(adventure)
                    remain_adventure_count -= 1
                break

    return result


def get_adventure_random_one(adventure_list, request_user):
    subquery_hero_metadata_id = HeroModel.query.\
        with_entities(HeroModel.hero_metadata_id).\
        filter(HeroModel.user_id == request_user.id).\
        filter(HeroModel.visible).\
        subquery()
    hero_names = MetadataHeroModel.query.\
        with_entities(MetadataHeroModel.name).\
        filter(MetadataHeroModel.id.in_(subquery_hero_metadata_id)).\
        all()

    options = []
    for adventure in adventure_list:
        curr_adventure_name = MetadataAdventureModel.query.\
            with_entities(MetadataAdventureModel.name).\
            filter(MetadataAdventureModel.id == adventure.adventure_metadata_id).\
            subquery()
        target = MetadataAdventureModel.query.\
            filter(MetadataAdventureModel.name == curr_adventure_name).\
            filter(and_(MetadataAdventureModel.level <= adventure.max_level,
                        MetadataAdventureModel.level >= adventure.max_level-3)).\
            filter(or_(MetadataAdventureModel.hero_name_for_appear.in_(hero_names),
                       MetadataAdventureModel.hero_name_for_appear == None)).\
            order_by(func.random()).\
            first()
        if target:
            options.append(target)
            print(target.id)
            adventure.adventure_metadata_id = target.id

    adventure_execution_refresh(adventure_list, request_user)

    remain_adventure_count = 1

    result = None

    while remain_adventure_count != 0 and len(options) != 0:
        choice = weighted_random(options,
                                 [adventure.appear_rate for adventure in options],
                                 sum(adventure.appear_rate for adventure in options))

        for adventure in adventure_list:
            if adventure.adventure_metadata_id == choice.id:
                if adventure.execution_count != choice.execution_limit:
                    result = adventure
                    remain_adventure_count -= 1
                break

    return result
