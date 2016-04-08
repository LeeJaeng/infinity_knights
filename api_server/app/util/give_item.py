import random
from app.models.metadata.lottery import MetadataLotteryModel
from app.util.give_item_hero import give_item_hero
from app.util.give_item_equipment import give_item_equipment
from app.util.give_item_long_term import give_item_rune_stone, give_item_soul_stone
from app.util.give_item_long_term import give_item_honor_coin, give_item_ancient_coin
from app.util.give_item_long_term import give_item_group_soul_stone, give_item_gem
from app.util.give_item_long_term import give_item_dungeon_ticket, give_item_league_ticket
from app.util.give_item_game_property import give_item_game_property

"""
    # UTIL : 아이템 주기
    # DESCRIPTION
        # 리워드를 통해 해당하는 item이 어느 타입인지 확인 하고 타입에 맞게 제공
        # 한 개의 아이템을 받는 give_item과 여러개 받을 수 있는 give_item_iter가 있음

"""


def give_item(request_user, item):
    result = dict()
    lottery_list = []
    if item.type == 'equipment':
        equipment_list = []
        for i in range(0, item.amount):
            equip = give_item_equipment(request_user, item.target_metadata_id)
            equipment_list.append(item.target_metadata_id)
        result[item.type] = equip

    elif item.type == 'hero':
        hero_list = []
        for i in range(0, item.amount):
            hero = give_item_hero(request_user, item.target_metadata_id)
            hero_list.append(hero)
        result[item.type] = hero_list

    elif item.type.find('soul_stone') == 0:
        item_type = give_item_soul_stone(request_user, item.type, item.amount)
        result[item_type] = item.amount

    elif item.type.find('group_soul_stone') == 0:
        give_item_group_soul_stone(request_user, item.type, item.amount)
        result[item.type] = item.amount

    elif item.type == 'rune_stone':
        give_item_rune_stone(request_user, item.amount)
        result[item.type] = item.amount

    elif item.type == 'lottery':
        for i in range(0, item.amount):
            lottery = give_item_lottery(request_user, item.target_metadata_id)
            lottery_list.append(lottery)
        result[item.type] = lottery_list

    elif item.type == 'gem':
        give_item_gem(request_user, item.amount)
        result[item.type] = item.amount

    elif item.type == 'gold':
        result[item.type] = item.amount

    elif item.type == 'honor_coin':
        give_item_honor_coin(request_user, item.amount)
        result[item.type] = item.amount

    elif item.type == 'ancient_coin':
        give_item_ancient_coin(request_user, item.amount)
        result[item.type] = item.amount

    elif item.type == 'dungeon_ticket':
        give_item_dungeon_ticket(request_user, item.amount)
        result[item.type] = item.amount

    elif item.type == 'league_ticket':
        league_ticket = give_item_league_ticket(request_user, item.amount)
        if league_ticket != 0:
            result[item.type] = league_ticket

    elif item.type.find('game_property_change') == 0:
        give_item_game_property(request_user, item.type, item.amount)
        result[item.type] = [item.target_metadata_id, item.amount]

    elif item.type == 'roulette_ticket':
        result[item.type] = [item.target_metadata_id, item.amount]

    return result


def give_item_iter(request_user, item_list):
    result = dict()
    lottery_list = []
    for item in item_list:
        if item.type == 'equipment':
            equipment_list = []
            for i in range(0, item.amount):
                equip = give_item_equipment(request_user, item.target_metadata_id)
                equipment_list.append(item.target_metadata_id)
            result[item.type] = equip

        elif item.type == 'hero':
            hero_list = []
            for i in range(0, item.amount):
                hero = give_item_hero(request_user, item.target_metadata_id)
                hero_list.append(hero)
            result[item.type] = hero_list

        elif item.type.find('soul_stone') == 0:
            item_type = give_item_soul_stone(request_user, item.type, item.amount)
            result[item_type] = item.amount

        elif item.type.find('group_soul_stone') == 0:
            give_item_group_soul_stone(request_user, item.type, item.amount)
            result[item.type] = item.amount

        elif item.type == 'rune_stone':
            give_item_rune_stone(request_user, item.amount)
            result[item.type] = item.amount

        elif item.type == 'lottery':
            i = 0
            while i < item.amount:
                lottery = give_item_lottery(request_user, item.target_metadata_id)
                lottery_list.append(lottery)
                i += 1
            result[item.type] = lottery_list

        elif item.type == 'gold':
            result[item.type] = item.amount

        elif item.type == 'gem':
            give_item_gem(request_user, item.amount)
            result[item.type] = item.amount

        elif item.type == 'honor_coin':
            give_item_honor_coin(request_user, item.amount)
            result[item.type] = item.amount

        elif item.type == 'ancient_coin':
            give_item_ancient_coin(request_user, item.amount)
            result[item.type] = item.amount

        elif item.type == 'dungeon_ticket':
            give_item_dungeon_ticket(request_user, item.amount)
            result[item.type] = item.amount

        elif item.type == 'league_ticket':
            league_ticket = give_item_league_ticket(request_user, item.amount)
            if league_ticket != 0:
                result[item.type] = league_ticket

        elif item.type.find('game_property_change') == 0:
            give_item_game_property(request_user, item.type, item.amount)
            result[item.type] = [item.target_metadata_id, item.amount]

        elif item.type == 'roulette_ticket':
            result[item.type] = [item.target_metadata_id, item.amount]

    return result



def weighted_random(li, choices, ratio_sum):
    r = random.uniform(0, ratio_sum)
    up = 0
    for i in range(0, len(choices)):
        if up + choices[i] >= r:
            return li[i]
        up += choices[i]


# TODO : Refactoring
def give_item_lottery(request_user, group_id):
    result = dict()
    metadata_lottery = MetadataLotteryModel.query.\
        filter(MetadataLotteryModel.group_id == group_id).\
        all()
    if metadata_lottery is None:
        return result
    item = weighted_random(metadata_lottery,
                           [metadata.weight for metadata in metadata_lottery],
                           sum(metadata.weight for metadata in metadata_lottery))

    result = give_item(request_user, item)
    return result
