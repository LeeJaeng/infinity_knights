from app.models.hero import HeroModel
from app.models.dungeon_activity import DungeonActivityModel
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.metadata.hero import MetadataHeroModel
from app import get_constant_value, CONSTANTS_KEY_HERO_MAX_GRADE
from app.util.set_user_achievement_value import accrue_user_achievement_value
from flask.ext.restful import abort


def give_item_rune_stone(request_user, amount):
    # add to user_achievement 'accrue_rune_stone'
    accrue_user_achievement_value(request_user, 'accrue_rune_stone', amount)
    request_user.rune_stone += amount


def give_item_gem(request_user, amount):
    request_user.gem += amount


def give_item_honor_coin(request_user, amount):
    accrue_user_achievement_value(request_user, 'accrue_honor_coin', amount)
    request_user.honor_coin += amount


def give_item_ancient_coin(request_user, amount):
    accrue_user_achievement_value(request_user, 'accrue_ancient_coin', amount)
    request_user.ancient_coin += amount


def give_item_soul_stone(request_user, soul_stone, amount):
    hero_name = soul_stone.split('soul_stone_')[1]
    subquery_hero_name = MetadataHeroModel.query.\
        with_entities(MetadataHeroModel.id).\
        filter(MetadataHeroModel.name == hero_name).\
        subquery()
    hero = HeroModel.query. \
        filter(HeroModel.user_id == request_user.id).\
        filter(HeroModel.hero_metadata_id.in_(subquery_hero_name)).\
        first()
    if hero is None:
        abort(400)

    metadata_hero = MetadataHeroModel.query.\
        with_entities(MetadataHeroModel.grade, MetadataHeroModel.group).\
        filter(MetadataHeroModel.id == hero.hero_metadata_id).\
        first()

    item_type = soul_stone
    if metadata_hero.grade == get_constant_value(CONSTANTS_KEY_HERO_MAX_GRADE):
        curr_g_soul_stone = getattr(request_user, 'group_soul_stone_{}'.format(metadata_hero.group))
        setattr(request_user, 'group_soul_stone_{}'.format(metadata_hero.group), curr_g_soul_stone + amount)
        item_type = 'group_soul_stone_{}'.format(metadata_hero.group)
    else:
        hero.soul_stone += amount

    return item_type


def give_item_group_soul_stone(request_user, group_soul_stone, amount):
    setattr(request_user, group_soul_stone, amount)


def give_item_dungeon_ticket(request_user, amount):
    dungeon_activity = DungeonActivityModel.query.\
        filter(DungeonActivityModel.user_id == request_user.id).\
        first()
    if dungeon_activity is None:
        abort(400)

    dungeon_activity.ticket += amount


def give_item_league_ticket(request_user, amount):
    league_ticket = 0
    league_property = LeagueUserPropertyModel.query.\
        filter(LeagueUserPropertyModel.user_id == request_user.id).\
        first()
    if league_property:
        league_property.ticket += amount
        league_ticket = amount
    return  league_ticket

