from app.models.metadata.reward import MetadataRewardModel
from flask.ext.restful import abort
from app.util.give_item import give_item_iter

"""
    # UTIL : 리워드 받기
    # DESCRIPTION
        # 리워드 이름을 넣고 호출하면 그 reward에 해당하는 보상 제공

"""


def get_reward(request_user, reward_name):
    rewards = MetadataRewardModel.query.\
        filter(MetadataRewardModel.name == reward_name).\
        all()
    if rewards is None or len(rewards) == 0:
        abort(400)

    result = give_item_iter(request_user, rewards)

    return result

