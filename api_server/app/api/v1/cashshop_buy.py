from app import api_root, db, access_token_required
from app.models.metadata.cashshop import MetadataCashShopItemModel
from app.models.cash_shop_history import CashShopHistoryModel
from app.util.get_reward import get_reward
from app.util.set_user_achievement_value import accrue_user_achievement_value
from flask.ext.restful import Resource, request, abort

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
scopes = ['https://www.googleapis.com/auth/androidpublisher']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'app/google/Idletower-174c42ca2fb9.json', scopes)
http_auth = credentials.authorize(Http())


"""
    # API : 캐쉬샵 물품 구입
    # DESCRIPTION
        # 캐쉬샵 물품을 구입하고 Reward 형식으로 반환
        # 캐쉬샵 구매 누적 업적 추가

"""


@api_root.resource('/v1/cash-shop/buy')
class CashShopBuy(Resource):
    @access_token_required
    def get(self, request_user):
        if 'item_id' not in request.args:
            abort(400)

        item_id = int(request.args['item_id'])

        target_item = MetadataCashShopItemModel.query. \
            filter(MetadataCashShopItemModel.id == item_id). \
            first()
        if target_item is None:
            abort(404)

        if target_item.cost_type == 'gem':
            if request_user.gem < target_item.cost:
                return {
                    'success': False,
                    'message': 'not enough gem'
                }
            request_user.gem -= target_item.cost

        result = get_reward(request_user, target_item.reward_name)
        # 구매 시 업적에 등록
        accrue_user_achievement_value(request_user, 'buy_goods_cash_shop', 1)

        # 구매 히스토리 등록
        history = CashShopHistoryModel(
            user_id=request_user.id,
            item_id=item_id
        )
        db.session.add(history)
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }

    @access_token_required
    def post(self, request_user):
        productId = request.json['productId']
        packageName = request.json['packageName']
        token = request.json['token']
        item_id = request.json['item_id']

        androidpublisher = build('androidpublisher', 'v2', credentials=credentials, http=http_auth)
        product = androidpublisher.purchases().products().\
            get(productId=productId, packageName=packageName, token=token)

        purchase = product.execute()

        print(dir(purchase))

        return 'success'
