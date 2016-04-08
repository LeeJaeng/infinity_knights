import uuid

from app import api_root, db
from app.util.get_hero_list import get_hero_list
from app.util.get_equipment_list import get_equipment_list
from app.util.return_generator import get_equipment_return
from app.models.user import UserModel
from app.models.artifact import ArtifactModel
from app.models.dungeon_activity import DungeonActivityModel
from app.models.user_short_term_property import UserShortTermPropertyModel
from app.models.metadata.artifact_option import MetadataArtifactOptionModel
from app.models.adventure import AdventureModel
from flask import request, abort
from flask.ext.restful import Resource

"""
    # API : 로그인
    # DESCRIPTION
        # uuid를 이용하여서 새로운 access token지급 받음

"""


@api_root.resource('/v1/auth/signin')
class SignIn(Resource):
    def get_list_hero(self, user):
        hero_list = []
        heroes = get_hero_list(user.id)
        for hero in heroes:
            hero_list.append({
                'id': hero.id,
                'hero_metadata_id': hero.hero_metadata_id,
                'enchant_level': hero.enchant_level,
                'soul_stone': hero.soul_stone,
                'skill_1_level': hero.skill_1_level,
                'skill_2_level': hero.skill_2_level,
                'skill_3_level': hero.skill_3_level,
                'equipment_id_weapon': hero.equipment_id_weapon,
                'equipment_id_accessory': hero.equipment_id_accessory,
                'visible': hero.visible
            })
        return hero_list

    def get_list_adventure(self, user):
        adventures = AdventureModel.query.\
            filter(AdventureModel.user_id == user.id). \
            all()

        adventure_list = []
        for adventure in adventures:
            adventure_list.append({
                'id': adventure.id,
                'adventure_metadata_id': adventure.adventure_metadata_id,
                'is_start': adventure.is_start,
                'hero_1_id': adventure.hero_1_id,
                'hero_2_id': adventure.hero_2_id,
                'hero_3_id': adventure.hero_3_id,
                'visible': adventure.visible,
                'max_level': adventure.max_level,
                'execution_count': adventure.execution_count
            })
        return adventure_list

    def get_list_user_property(self, user):
        long_term_property_list = ['rune_stone', 'group_soul_stone_human', 'group_soul_stone_orc', 'group_soul_stone_elf', 'group_soul_stone_furry', 'gem', 'ancient_coin', 'honor_coin']
        short_term_property_list = ['gold', 'world', 'stage', 'accrue_stage', 'quest', 'quest_level', 'quest_auto', 'quest_start_time', 'hero_party_stage', 'hero_level_stage', 'hero_party_dungeon']
        short_term_property = UserShortTermPropertyModel.query.\
            filter(UserShortTermPropertyModel.user_id == user.id).\
            first()

        result = dict()
        for i in range(0, len(long_term_property_list)):
            result[long_term_property_list[i]] = getattr(user, long_term_property_list[i])

        for i in range(0, len(short_term_property_list)):
            result[short_term_property_list[i]] = getattr(short_term_property, short_term_property_list[i])

        dungeon_activity = DungeonActivityModel.query.\
            with_entities(DungeonActivityModel.ticket).\
            filter(DungeonActivityModel.user_id == user.id).\
            first()
        result['dungeon_ticket'] = dungeon_activity.ticket

        return result

    def get_list_equipment(self, user):
        equipments = get_equipment_list(user.id)
        equipment_list = []

        if equipments is None:
            return equipment_list

        for equipment in equipments:
            equipment_list.append(get_equipment_return(equipment.id))

        return equipment_list

    def get_list_artifact(self, user):
        artifacts = ArtifactModel.query. \
            filter(ArtifactModel.user_id == user.id). \
            all()

        artifact_metadata_id_list = [item.artifact_metadata_id for item in artifacts]
        artifact_option_metadata_list = MetadataArtifactOptionModel.query. \
            filter(MetadataArtifactOptionModel.artifact_metadata_id.in_(artifact_metadata_id_list)). \
            all()

        artifact_list = []
        for item in artifacts:
            elem = dict()
            elem['id'] = item.id
            elem['artifact_metadata_id'] = item.artifact_metadata_id
            elem['level'] = item.level
            elem['options'] = [option.id for option in artifact_option_metadata_list
                               if option.artifact_metadata_id == item.artifact_metadata_id]
            artifact_list.append(elem)

        return artifact_list

    def post(self):
        if 'uuid' not in request.json:
            abort(400)

        try:
            uuid.UUID(request.json['uuid'], version=4)
        except ValueError:
            abort(400)

        user = UserModel.query.\
            filter(UserModel.uuid == request.json['uuid']).\
            first()

        if user is None:
            abort(404)

        user.access_token = uuid.uuid4()

        result = dict()
        # hero 주기
        result['hero'] = self.get_list_hero(user)

        # user property 주기
        result['user_property'] = self.get_list_user_property(user)

        # 모험 주기
        result['adventure'] = self.get_list_adventure(user)

        # 장비 주기
        result['equipment'] = self.get_list_equipment(user)

        # 유물 주기
        result['artifact'] = self.get_list_artifact(user)

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'access_token': str(user.access_token),
            'result': result
        }
