from app import api_root, db, access_token_required
from app.models.metadata.honor_shop import MetadataHonorShopModel
from app.util.give_item import give_item
from app.util.set_user_achievement_value import accrue_user_achievement_value
from flask.ext.restful import Resource, request, abort

"""
    # API : 명예 상점 물품 구매
    # DESCRIPTION
        # 명예 점수(리그에서 획득)를 가지고 물품 구입
        # 명예 상점 누적 구매 업적 추가

"""


@api_root.resource('/v1/honor-shop/buy')
class HonorShopBuy(Resource):
    @access_token_required
    def get(self, request_user):
        if 'honor_shop_item_metadata_id' not in request.args:
            abort(400)

        honor_shop_item_metadata_id = int(request.args['honor_shop_item_metadata_id'])
        honor_shop_item_metadata = MetadataHonorShopModel.query.\
            filter(MetadataHonorShopModel.id == honor_shop_item_metadata_id).\
            first()
        if honor_shop_item_metadata is None:
            abort(404)

        if request_user.honor_coin < honor_shop_item_metadata.cost:
            return {
                'success': False,
                'message': 'not enough honor coin'
            }

        request_user.honor_coin -= honor_shop_item_metadata.cost
        result = give_item(request_user, honor_shop_item_metadata)
        # 구매 시 업적에 등록
        accrue_user_achievement_value(request_user, 'buy_goods_honor_shop', 1)

        db.session.commit()

        # TODO: marshalling
        return {
            'success': True,
            'honor_coin': request_user.honor_coin,
            'result': result
        }
