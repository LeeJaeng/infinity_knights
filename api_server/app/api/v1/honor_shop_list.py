from app import api_root, db, access_token_required
from app.models.metadata.honor_shop import MetadataHonorShopModel
from flask.ext.restful import Resource, abort

"""
    # API : 명예 상점 물품 목록
    # DESCRIPTION
        # 명예 상점 물품 id만 제공

"""


@api_root.resource('/v1/honor-shop')
class HonorShopList(Resource):
    @access_token_required
    def get(self, request_user):
        # 일단 메타데이터 id만 주기
        honor_shop_item_list = MetadataHonorShopModel.query.\
            with_entities(MetadataHonorShopModel.id).\
            all()
        if honor_shop_item_list is None:
            abort(404)

        result = [item.id for item in honor_shop_item_list]

        return {
            'success': True,
            'result': result
        }
