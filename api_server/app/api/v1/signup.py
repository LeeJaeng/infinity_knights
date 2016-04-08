import random
from datetime import datetime

from app import api_root, db, get_constant_value, CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_SIZE, \
    CONSTANTS_KEY_DEFAULT_HERO_METADATA_ID
from app.util.give_item_equipment import give_item_equipment
from app.util.give_hero_basic_equipment import give_hero_basic_equipment
from app.models.dungeon_activity import DungeonActivityModel
from app.models.user_achievement import UserAchievementModel
from app.models.metadata.artifact import MetadataArtifactModel
from app.models.user_short_term_property import UserShortTermPropertyModel
from app.models.user import UserModel
from app.models.artifact_show_window import ArtifactShowWindowModel
from app.models.metadata.hero import MetadataHeroModel
from app.models.hero import HeroModel
from app.models.metadata.adventure import MetadataAdventureModel
from app.models.adventure import AdventureModel
from app.models.constants import ConstantsModel
from app.models.purchase_verification import PurchaseVerificationModel
from flask.ext.restful import Resource, request

"""
    # API : 회원가입
    # DESCRIPTION
        # 유저 모델 생성
        # Time gap 설정 (UTC와의 시간 차이)
        # 던전 Activity 모델 생성
        # 유물 쇼 윈도우 모델 생성
        # 영웅 모델 생성 (기본 영웅/장비 지급)
        # 모험 모델 생성
        # 유저 업적 모델 생성

"""


@api_root.resource('/v1/auth/signup')
class SignUp(Resource):
    def post(self):
        # User 생성
        new_user = UserModel()
        db.session.add(new_user)
        db.session.commit()

        # User Nickname 생성
        new_user.nickname = 'user{}'.format(new_user.id)

        # Time gap 설정
        curr_utc_date = datetime.utcnow()
        local_date_str = request.json['local_date']
        local_date = datetime.strptime(local_date_str, "%Y-%m-%d %H:%M:%S")
        time_diff = local_date - curr_utc_date
        time_gap = round(time_diff.total_seconds() / 3600)
        new_user.time_gap = time_gap

        # 던전 Activity 생성
        dungeon_activity = DungeonActivityModel(user_id=new_user.id,
                                                ticket=5,
                                                max_ticket=5)
        db.session.add(dungeon_activity)

        # 유물 쇼 윈도우 리스트 생성
        total_artifact_metadata = MetadataArtifactModel.query.all()
        total_artifact_metadata_id_list = [item.id for item in total_artifact_metadata]
        for i in range(0, get_constant_value(CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_SIZE)):
            artifact_metadata_id = random.choice(total_artifact_metadata_id_list)
            total_artifact_metadata_id_list.remove(artifact_metadata_id)

            artifact_show_window_item = ArtifactShowWindowModel(user_id=new_user.id,
                                                                artifact_metadata_id=artifact_metadata_id)
            db.session.add(artifact_show_window_item)


        # 영웅 리스트 생성
        # 1. 기본 등급의 영웅들을 생성한다.
        # 2. 그 중 기본 지급 영웅들은 visible을 true로
        total_hero_metadata = MetadataHeroModel.query.\
            filter(MetadataHeroModel.is_basic_grade).\
            all()

        # TODO : remove at release
        for hero_metadata in total_hero_metadata:
            new_hero = HeroModel(
                user_id=new_user.id,
                hero_metadata_id=hero_metadata.id,
                visible=False,
                soul_stone=10000
            )
            db.session.add(new_hero)
        db.session.commit()

        # 기본 영웅들에게 장비 지급 해주고 visible을 True시킨다
        default_heroes = ConstantsModel.query.\
            with_entities(ConstantsModel.value).\
            filter(ConstantsModel.key == CONSTANTS_KEY_DEFAULT_HERO_METADATA_ID).\
            all()
        default_hero_list = list()
        for default_hero in default_heroes:
            default_hero_list.append(default_hero.value)
        default_heroes = HeroModel.query. \
            filter(HeroModel.user_id == new_user.id).\
            filter(HeroModel.hero_metadata_id.in_(default_hero_list)).\
            all()
        for default_hero in default_heroes:
            default_hero.visible = True
            give_hero_basic_equipment(new_user, default_hero)

        # 모험 모델 생성
        total_adventure_metadata = MetadataAdventureModel.query.\
            filter(MetadataAdventureModel.level == 1).\
            all()

        for adventure_metadata in total_adventure_metadata:
            new_adventure = AdventureModel(
                user_id=new_user.id,
                adventure_metadata_id=adventure_metadata.id
            )
            db.session.add(new_adventure)

        # 유저 업적 모델 생성
        user_achievement = UserAchievementModel(
            user_id=new_user.id
        )
        db.session.add(user_achievement)

        user_short_term_property = UserShortTermPropertyModel(
            user_id=new_user.id
        )
        db.session.add(user_short_term_property)

        # generate purchase verification model
        purchase_verification = PurchaseVerificationModel(
            user_id=new_user.id
        )
        db.session.add(purchase_verification)

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'uuid': str(new_user.uuid),
        }
