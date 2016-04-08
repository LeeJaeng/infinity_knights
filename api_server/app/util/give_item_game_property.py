from app.models.adventure import AdventureModel
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.dungeon_activity import DungeonActivityModel
from enum import Enum


class Properties(Enum):
    adventurer_boots = 1
    hermes_boots = 2
    goddess_blessing = 3
    dungeon_max_ticket_increase = 4
    league_max_ticket_increase = 5
    hero_movspd_increase = 6
    hero_atk_increase = 7
    earn_gold_increase = 8


def give_item_game_property(request_user, game_property, amount):

    print(game_property)
    property_type = int(game_property.split('game_property_change_')[1])

    # 모험 시간 감소 (%)
    if property_type == Properties.adventurer_boots:
        adventures = AdventureModel.query.\
            filter(AdventureModel.user_id == request_user.id).\
            all()
        for adventure in adventures:
            adventure.duration_decrease_rate = amount
        return

    # 스텝 감소 (정수)
    elif property_type == Properties.hermes_boots:
        return

    # 환생시 룬스톤 양 증가 (%)
    elif property_type == Properties.goddess_blessing:
        return

    # 던전 최대 티켓 +1
    elif property_type == Properties.dungeon_max_ticket_increase:
        dungeon_activity = DungeonActivityModel.query.\
            filter(DungeonActivityModel.user_id == request_user.id).\
            first()
        dungeon_activity.max_ticket += amount
        return

    # 리그 최대 티켓 +1
    elif property_type == Properties.league_max_ticket_increase:
        league_property = LeagueUserPropertyModel.query.\
            filter(LeagueUserPropertyModel.user_id == request_user.id).\
            first()
        league_property.max_ticket += amount
        return

    # 영웅들 이동속도 증가 (%)
    elif property_type == Properties.hero_movspd_increase:
        return

    # 영웅들 공격력 증가 (%)
    elif property_type == Properties.hero_atk_increase:
        return

    # 골드 획득 증가 (몬스터 처치 골드 획득량, 퀘스트 완료 골드 획득량 % 증가
    elif property_type == Properties.earn_gold_increase:
        return
