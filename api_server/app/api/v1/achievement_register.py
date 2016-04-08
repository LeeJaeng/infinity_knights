from app import db, api_root, access_token_required
from app import get_constant_value, CONSTANTS_KEY_HERO_MAX_GRADE
from app.util.get_reward import get_reward
from app.models.artifact import ArtifactModel
from app.models.hero import HeroModel
from app.models.metadata.hero import MetadataHeroModel
from app.models.achievement import AchievementModel
from app.models.metadata.achievement import MetadataAchievementModel
from app.models.user_achievement import UserAchievementModel
from flask.ext.restful import Resource, request, abort

"""
    # API : 업적 등록
    # DESCRIPTION
        # 유저가 달성한 업적을 보상받기 위함
        # 업적을 받기에 합당한 지 확인하는 함수가 있음

"""


@api_root.resource('/v1/achievements/register')
class AchievementRegister(Resource):
    @access_token_required
    def get(self, request_user):
        if 'achievement_metadata_id' not in request.args:
            abort(400)

        metadata_achievement_id = int(request.args['achievement_metadata_id'])

        metadata_achievement = MetadataAchievementModel.query.\
            filter(MetadataAchievementModel.id == metadata_achievement_id).\
            first()

        # 업적을 등록시키에 합당한지 확인 한다.
        if type_value_validation(request_user.id, metadata_achievement):
            result = get_reward(request_user, metadata_achievement.reward_name)
            achievement = AchievementModel(
                user_id=request_user.id,
                achievement_metadata_id=metadata_achievement_id
            )
            db.session.add(achievement)
        else:
            return {
                'success': False,
                'message': 'not meeting the requirements'
            }

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }


# 각 업적 종류에 따라서 현재 유저가 업적을 받기에 합당한 지를 확인한다
def type_value_validation(user_id, achievement):
    in_user_achievement = ['stage_world_1', 'stage_world_2', 'accrue_rune_stone', 'accrue_honor_coin',
                           'accrue_ancient_coin', 'accrue_breakthrough', 'max_hero_level', 'max_hero_enchant',
                           'league_try', 'league_win', 'adventure_try', 'adventure_try', 'adventure_success',
                           'buy_goods_honor_shop', 'buy_goods_cash_shop', 'accrue_rebirth']

    result = False

    if achievement.type in in_user_achievement:
        user_achievement = UserAchievementModel.query.filter(UserAchievementModel.id == user_id).first()
        if achievement.value <= getattr(user_achievement, achievement.type):
            result = True
        # TODO: delete at release
        print("achievement value : {0},   {1} : {2}".format(achievement.value, achievement.type, getattr(user_achievement, achievement.type)))

    if achievement.type == 'possess_hero_all':
        heroes = HeroModel.query.\
            filter(HeroModel.user_id == user_id). \
            filter(HeroModel.visible).\
            count()
        if achievement.value <= heroes:
            result = True
        print("achievement value : {0},   {1} : {2}".format(achievement.value, achievement.type, heroes))

    if achievement.type == 'possess_hero_evolve':
        subquery_hero_metadata_id = HeroModel.query.\
            with_entities(HeroModel.hero_metadata_id).\
            filter(HeroModel.user_id == user_id).\
            subquery()
        heroes_evolve = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id.in_(subquery_hero_metadata_id)). \
            filter(MetadataHeroModel.is_evolve).\
            count()
        if achievement.value <= heroes_evolve:
            result = True
        print("achievement value : {0},   {1} : {2}".format(achievement.value, achievement.type, heroes_evolve))

    if achievement.type == 'possess_hero_grade_5':
        subquery_hero_metadata_id = HeroModel.query.\
            with_entities(HeroModel.hero_metadata_id).\
            filter(HeroModel.user_id == user_id).\
            subquery()
        heroes_grade_5 = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id.in_(subquery_hero_metadata_id)). \
            filter(MetadataHeroModel.grade == get_constant_value(CONSTANTS_KEY_HERO_MAX_GRADE)).\
            count()
        if achievement.value <= heroes_grade_5:
            result = True
        print("achievement value : {0},   {1} : {2}".format(achievement.value, achievement.type, heroes_grade_5))

    elif achievement.type == 'possess_artifact':
        artifacts = ArtifactModel.query.\
            filter(ArtifactModel.user_id == user_id).\
            count()
        if achievement.value <= artifacts:
            result = True
        print("achievement value : {0},   {1} : {2}".format(achievement.value, achievement.type, len(artifacts)))
    return result
