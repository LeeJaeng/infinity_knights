from app.models.user_achievement import UserAchievementModel
from app import db

"""
    # UTIL : 유저 업적 모델에 등록
    # DESCRIPTION
        # 업적이 누적 되는 것이면 accrue_user_achievement
        # 업적이 갱신 되는 것이면 update_user_achievement

"""


# max value : [stage_world_1, stage_world_2, max_hero_level, max_hero_enchant]
def update_user_achievement_value(request_user, achievement_type, value):
    user_achievement = UserAchievementModel.query.\
        filter(UserAchievementModel.user_id == request_user.id).\
        first()

    curr_value = getattr(user_achievement, achievement_type)
    if curr_value < value:
        setattr(user_achievement, achievement_type, value)

    db.session.commit()


# others
def accrue_user_achievement_value(request_user, achievement_type, value):
    user_achievement = UserAchievementModel.query.\
        filter(UserAchievementModel.user_id == request_user.id).\
        first()

    curr_value = getattr(user_achievement, achievement_type)
    setattr(user_achievement, achievement_type, curr_value + value)

