import math
from app import api_root, db, access_token_required
from flask import request, abort
from flask.ext.restful import Resource
from app import get_constant_value, CONSTANTS_KEY_POWER_REVIVAL_GEM_COST
from app.util.set_user_achievement_value import accrue_user_achievement_value

"""
    # API : 환생
    # DESCRIPTION
        # Long term 재화를 제외한 모든 것 초기화
        # Power revival은 과금 재화인 gem 사용
        # 누적 환생 업적 추가

"""


@api_root.resource('/v1/revival')
class Revival(Resource):
    @access_token_required
    def get(self, request_user):
        if 'power_revival' not in request.args:
            abort(400)
        if 'reward_rune' not in request.args:
            abort(400)
        power_revival = request.args['power_revival']
        reward_rune = float(request.args['reward_rune'])
        reward_rune = math.floor(reward_rune)

        # 강화된 환생이면 User의 gem을 깎는다
        if power_revival == 'true':
            if request_user.gem < get_constant_value(CONSTANTS_KEY_POWER_REVIVAL_GEM_COST):
                return {
                    'success': False,
                    'message': 'not enough gem'
                }
            request_user.gem -= get_constant_value(CONSTANTS_KEY_POWER_REVIVAL_GEM_COST)

        request_user.rune_stone += reward_rune

        # add to 업적 'accrue_rune_stone', 환생
        accrue_user_achievement_value(request_user, 'accrue_rune_stone', reward_rune)
        accrue_user_achievement_value(request_user, 'accrue_rebirth', 1)

        # 영웅 레벨 초기화 및 생산시설 초기화는 클라이언트에서
        db.session.commit()

        return {
            'success': True,
            'rune_stone': request_user.rune_stone,
            'power_revival': power_revival,
            'gem': request_user.gem
        }

