from app import api_root, access_token_required
from app.models.metadata.cashshop import MetadataCashShopItemModel
from app.models.cash_shop_history import CashShopHistoryModel
from flask.ext.restful import Resource

"""
    # API : 캐쉬샵 구매 리스트
    # DESCRIPTION
        # 캐쉬샵에서 구매할 수 있는 모든 제품 반환

"""


@api_root.resource('/v1/cash-shop')
class CashshopList(Resource):
    @access_token_required
    def get(self, request_user):
        cashshop_items = MetadataCashShopItemModel.query.\
            order_by(MetadataCashShopItemModel.id.asc()).\
            all()

        histories = CashShopHistoryModel.query.\
            with_entities(CashShopHistoryModel.item_id).\
            filter(CashShopHistoryModel.user_id == request_user.id).\
            all()

        purchased_item_id = []
        if histories is not None:
            purchased_item_id = [item.item_id for item in histories]

        items = []

        curr_item_group = ''
        for item in cashshop_items:
            if item.item_type == 'continual':
                items.append(item)
            elif item.item_type == 'ad_continual':
                items.append(item)
            elif item.item_type == 'one':
                if item.id in purchased_item_id:
                    continue
                else:
                    items.append(item)
            elif item.item_type == 'stepped':
                if item.id in purchased_item_id:
                    continue
                else:
                    if curr_item_group != item.item_group:
                        curr_item_group = item.item_group
                        items.append(item)
                    continue

        result = []
        if items is not None:
            result = [item.id for item in items]

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
