import random
from app.util.get_reward import get_reward
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from app.models.adventure_history import AdventureHistoryModel

"""
    # UTIL : 모험 결과 확인
    # DESCRIPTION
        # 모험이 끝났을 때 그 모험이 성공했는지 실패 했는지 성공률에 기반하여 계산
        # 성공 시 reward 제공

"""


def get_adventure_result(request_user, adventure, metadata_adventure):

    # 모험에 참가한 영웅들
    adventure_heroes = []
    for i in range(0, metadata_adventure.dispatch_number):
        hero_id = getattr(adventure, "hero_{}_id".format(i+1))
        hero = HeroModel.query.filter(HeroModel.id == hero_id).first()
        if hero is not None:
            adventure_heroes.append(hero)

    # 모험에 참가한 영웅들 메타데이터
    adventure_heroes_metadata = []
    for hero in adventure_heroes:
        metadata_hero = MetadataHeroModel.query.filter(MetadataHeroModel.id == hero.hero_metadata_id).first()
        adventure_heroes_metadata.append(metadata_hero)

    # TODO : constant에 추가
    success_limit = 100

    # 적정강화도 계산
    total_heroes_enchant_level = 0
    for hero in adventure_heroes:
        total_heroes_enchant_level += hero.enchant_level

    #  max( 0,    min(성공한계 레벨, (강화도 평균 - 적정강화도 + 성공한계 레벨))   /  성공 한계레벨 * (난이도 최대성공률 - 미달페널티))
    dispatch_number = metadata_adventure.dispatch_number
    suitable_difficulty = metadata_adventure.suitable_difficulty
    shortfall_penalty = metadata_adventure.shortfall_penalty
    maximum_success_rate = metadata_adventure.maximum_success_rate

    enchant_average = total_heroes_enchant_level / dispatch_number

    cal = min(success_limit, (enchant_average - suitable_difficulty + success_limit))
    success_rate = max (0, cal / success_limit * (maximum_success_rate - shortfall_penalty))

    # 특성 보너스 계산
    trait_bonus = 0
    for hero_metadata in adventure_heroes_metadata:
        if metadata_adventure.trait_grade is not None:
            break
        if metadata_adventure.trait_grade == hero_metadata.grade:
            trait_bonus += metadata_adventure.trait_grade_bonus
            break
    for hero_metadata in adventure_heroes_metadata:
        if metadata_adventure.trait_area is not None:
            break
        if metadata_adventure.trait_area == hero_metadata.area:
            trait_bonus += metadata_adventure.trait_area_bonus
            break
    for hero_metadata in adventure_heroes_metadata:
        if metadata_adventure.trait_group is not None:
            break
        if metadata_adventure.trait_group == hero_metadata.group:
            trait_bonus += metadata_adventure.trait_group_bonus
            break
    for hero_metadata in adventure_heroes_metadata:
        if metadata_adventure.trait_sex is not None:
            break
        if metadata_adventure.trait_sex == hero_metadata.sex:
            trait_bonus += metadata_adventure.trait_sex_bonus
            break
    for hero_metadata in adventure_heroes_metadata:
        if metadata_adventure.trait_class is not None:
            break
        if metadata_adventure.trait_class == hero_metadata.hero_class:
            trait_bonus += metadata_adventure.trait_class_bonus
            break

    # 성공 확률 계산
    success_rate += trait_bonus
    print('success rate : {}'.format(success_rate))

    # 성공 여부 확인
    select_box = ['success'] * int(success_rate) + ['failure'] * int(100-success_rate)
    choice = random.choice(select_box)

    success = False
    # 성공했을 때 초기화 과정
    if choice == 'success':
        success = True

    # 보상
    result = []
    final_reward = []
    main_reward = []
    additional_reward = []
    if success:
        # 마지막 Adventure을 처음으로 수행 했을 때 보상 주기
        if metadata_adventure.final_reward_name:
            adventure_history = AdventureHistoryModel.query.\
                filter(AdventureHistoryModel.user_id == request_user.id).\
                filter(AdventureHistoryModel.adventure_metadata_id == metadata_adventure.id).\
                first()
            if not adventure_history or not adventure_history.is_complete:
                final_reward = get_reward(request_user, metadata_adventure.final_reward_name)
        main_reward = get_reward(request_user, metadata_adventure.main_reward_name)
        if metadata_adventure.additional_reward_name:
            additional_reward = get_reward(request_user, metadata_adventure.additional_reward_name)
        success = True

    result.append(success)
    result.append(final_reward)
    result.append(main_reward)
    result.append(additional_reward)

    return result
