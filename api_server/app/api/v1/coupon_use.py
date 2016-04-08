from app import api_root, access_token_required, db
from app.models.coupon import CouponModel
from app.models.coupon_history import CouponHistoryModel
from app.util.get_reward import get_reward
from flask.ext.restful import Resource, request, abort

"""
    # API : 쿠폰 사용
    # DESCRIPTION
        # 미리 입력된 쿠폰을 유저가 입력했을 때 사용 가능
        # 쿠폰 히스토리 저장

"""


@api_root.resource('/v1/coupon-use')
class CouponUse(Resource):
    @access_token_required
    def get(self, request_user):
        if 'code' not in request.args:
            abort(400)
        coupon_code = request.args['code']

        coupon = CouponModel.query.\
            filter(CouponModel.code == coupon_code).\
            first()
        if coupon is None:
            abort(404)

        if coupon.stock == 0:
            return {
                'success': False,
                'message': 'coupon is stockless'
            }

        coupon_history = CouponHistoryModel.query.\
            filter(CouponHistoryModel.user_id == request_user.id).\
            filter(CouponHistoryModel.coupon_id == coupon.id).\
            first()
        if coupon_history is not None:
            return {
                'success': False,
                'message': 'Used coupon.'
            }

        result = get_reward(request_user, coupon.reward_name)

        if coupon.stock > 0:
            coupon.stock -= 1

        new_coupon_history = CouponHistoryModel(user_id=request_user.id, coupon_id=coupon.id)
        db.session.add(new_coupon_history)

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
