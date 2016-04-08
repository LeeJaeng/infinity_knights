from app import api_root, db, access_token_required
from flask import request, abort
from flask.ext.restful import Resource

"""
    # API : 퀘스트 자동 업그레이드
    # DESCRIPTION
        # 과금 재화인 gem을 이용하여 퀘스트 자동 업그레이드

"""


@api_root.resource('/v1/quest/auto-upgrade')
class QuestAutoUpgrade(Resource):
    @access_token_required
    def get(self, request_user):
        if 'cost' not in request.args:
            abort(400)
        cost_gem = int(request.args['cost'])

        if request_user.gem < cost_gem:
            return {
                'success': False,
                'message': 'not enough gem'
            }

        request_user.gem -= cost_gem
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'gem': request_user.gem
        }
