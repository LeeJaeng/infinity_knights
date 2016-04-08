from app import db
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.hero import HeroModel
from app.models.equipment import EquipmentModel
from app.models.equipment_option import EquipmentOptionModel
from app.models.user import UserModel
from sqlalchemy.sql import func


def get_league_opponent(my_elo, league_id, request_user):
    opponent = LeagueUserPropertyModel.query. \
        filter(LeagueUserPropertyModel.league_id == league_id). \
        filter(LeagueUserPropertyModel.user_id != request_user.id). \
        filter(LeagueUserPropertyModel.hero_party != None). \
        filter(LeagueUserPropertyModel.elo <= my_elo + 100). \
        filter(LeagueUserPropertyModel.elo >= my_elo - 100). \
        order_by(func.random()).\
        first()

    count = 2
    while opponent is None:
        opponent = LeagueUserPropertyModel.query. \
            filter(LeagueUserPropertyModel.league_id == league_id). \
            filter(LeagueUserPropertyModel.user_id != request_user.id). \
            filter(LeagueUserPropertyModel.hero_party != None). \
            filter(LeagueUserPropertyModel.elo <= my_elo + 100 * count). \
            filter(LeagueUserPropertyModel.elo >= my_elo - 100 * count). \
            order_by(func.random()). \
            first()
        count += 1
        if count == 10:
            break

    return opponent


# 상대방의 히어로, 장비, 장비 옵션을 얻는 함수
def get_league_opponent_info(league_id, opponent_id):
    opponent_nickname, opponent_property = db.session.query(UserModel.nickname, LeagueUserPropertyModel).\
        join(LeagueUserPropertyModel). \
        filter(UserModel.id == opponent_id).\
        filter(LeagueUserPropertyModel.league_id == league_id).\
        first()

    opponent_hero_list = []
    opponent_hero_id_list = []
    opponent_hero = HeroModel.query.\
        filter(HeroModel.id.in_(opponent_property.hero_party)).\
        all()

    for hero in opponent_hero:
        opponent_hero_id_list.append(hero.id)
        opponent_hero_list.append(
            {
                'id': hero.id,
                'hero_metadata_id': hero.hero_metadata_id,
                'enchant_level': hero.enchant_level,
                'skill_1_level': hero.skill_1_level,
                'skill_2_level': hero.skill_2_level,
                'skill_3_level': hero.skill_3_level,
                'equipment_id_weapon': hero.equipment_id_weapon,
                'equipment_id_accessory': hero.equipment_id_accessory,
            }
        )

    opponent_equipment = EquipmentModel.query.\
        filter(EquipmentModel.hero_id.in_(opponent_hero_id_list)).\
        order_by(EquipmentModel.id.asc()).\
        all()

    opponent_equipment_list = []
    for equipment in opponent_equipment:
        equipment_options = EquipmentOptionModel.query.\
            filter(EquipmentOptionModel.equipment_id == equipment.id).\
            order_by(EquipmentOptionModel.id.asc()).\
            all()
        option_id_list = []
        option_value_list = []
        for option in equipment_options:
            option_id_list.append(option.option_metadata_id)
            option_value_list.append(option.value)

        result = {
            'id': equipment.id,
            'hero_id': equipment.hero_id,
            'equipment_metadata_id': equipment.equipment_metadata_id,
            'enchant_level': equipment.enchant_level,
            'equipment_option_id_list': option_id_list,
            'equipment_option_value_list': option_value_list,
        }
        opponent_equipment_list.append(result)

    result = dict()
    result['nickname'] = opponent_nickname
    result['elo'] = opponent_property.elo
    result['win'] = opponent_property.win
    result['lose'] = opponent_property.lose
    result['draw'] = opponent_property.draw
    result['hero_party'] = opponent_hero_list
    result['hero_equipment'] = opponent_equipment_list

    return result
