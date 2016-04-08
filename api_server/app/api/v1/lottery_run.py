import random

from app import api_root, db, access_token_required
from app.util.give_item import give_item
from app.models.metadata.lottery import MetadataLotteryModel
from flask.ext.restful import Resource, request

"""
    # API : 복권 실행
    # DESCRIPTION
        # group_id가 맞는 복권 실행
        # 가중치에 맞게 실행하도록 하는 함수 작성

"""


def weighted_random(li, choices, ratio_sum):
        r = random.uniform(0, ratio_sum)
        up = 0
        for i in range(0, len(choices)):
            if up + choices[i] >= r:
                return li[i]
            up += choices[i]


@api_root.resource('/v1/lottery/run')
class LotteryRun(Resource):
    @access_token_required
    def get(self, request_user):
        group_id = request.args['group_id']

        metadata_lottery = MetadataLotteryModel.query.\
            filter(MetadataLotteryModel.group_id == group_id).\
            all()
        random_metadata = weighted_random(metadata_lottery,
                                          [metadata.weight for metadata in metadata_lottery],
                                          sum(metadata.weight for metadata in metadata_lottery))

        result = give_item(request_user, random_metadata)
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
