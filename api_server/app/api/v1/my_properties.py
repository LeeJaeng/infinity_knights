from app import api_root, access_token_required, db
from app.models.dungeon_activity import DungeonActivityModel
from app.models.user_short_term_property import UserShortTermPropertyModel
from app.models.user_achievement import UserAchievementModel
from flask import request
from flask.ext.restful import Resource

"""
    # API : GET(유저 재화 조회) POST(Short term 재화 등록)
    # DESCRIPTION
        # GET : Short term, Long term, 재화 조회
        # POST : Short term 재화 서버에 업데이트

"""


long_term_property_list = ['rune_stone', 'group_soul_stone_human', 'group_soul_stone_orc', 'group_soul_stone_elf', 'group_soul_stone_furry', 'gem', 'ancient_coin', 'honor_coin']
short_term_property_list = ['gold', 'world', 'stage', 'accrue_stage', 'quest', 'quest_level', 'quest_auto', 'quest_start_time', 'hero_party_stage', 'hero_level_stage', 'hero_party_dungeon']

@api_root.resource('/v1/my-properties')
class MyProperties(Resource):
    @access_token_required
    def get(self, request_user):
        short_term_property = UserShortTermPropertyModel.query.\
            filter(UserShortTermPropertyModel.user_id == request_user.id).\
            first()

        result = dict()
        for i in range(0, len(long_term_property_list)):
            result[long_term_property_list[i]] = getattr(request_user, long_term_property_list[i])

        for i in range(0, len(short_term_property_list)):
            result[short_term_property_list[i]] = getattr(short_term_property, short_term_property_list[i])

        dungeon_activity = DungeonActivityModel.query.\
            with_entities(DungeonActivityModel.ticket).\
            filter(DungeonActivityModel.user_id == request_user.id).\
            first()

        result['dungeon_ticket'] = dungeon_activity.ticket

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }

    @access_token_required
    def post(self, request_user):

        user_property = UserShortTermPropertyModel.query.\
            filter(UserShortTermPropertyModel.user_id == request_user.id).\
            first()

        for i in range(0, len(short_term_property_list)):
            value = request.json[short_term_property_list[i]]
            setattr(user_property, short_term_property_list[i], value)

        # world_1_stage, world_2_stage, max_hero_level 를 user_achievement에 등록
        user_achievement = UserAchievementModel.query.\
            filter(UserAchievementModel.user_id == request_user.id).\
            first()

        if user_property.world == 1:
            if user_property.stage > user_achievement.stage_world_1:
                user_achievement.stage_world_1 = user_property.stage
        elif user_property.world == 2:
            if user_property.stage > user_achievement.stage_world_2:
                user_achievement.stage_world_2 = user_property.stage

        hero_level_list = user_property.hero_level_stage
        hero_level_list.sort()
        max_level = hero_level_list[len(hero_level_list)-1]

        if max_level > user_achievement.max_hero_level:
            user_achievement.max_hero_level = max_level

        db.session.commit()

        return {
            'success': True,
        }
