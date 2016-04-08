from app import api_root, db, access_token_required
from app.models.artifact import ArtifactModel
from app.models.artifact_show_window import ArtifactShowWindowModel
from app.models.metadata.artifact import MetadataArtifactModel
from flask.ext.restful import Resource, request, abort

"""
    # API : 유물 구매
    # DESCRIPTION
        # 유물 쇼 윈도우에서 선택된 유물을 구매

"""


@api_root.resource('/v1/artifacts/buy')
class ArtifactBuy(Resource):
    @access_token_required
    def get(self, request_user):
        if 'artifact_metadata_id' not in request.args:
            abort(400)

        artifact_metadata_id = int(request.args['artifact_metadata_id'])
        artifact_metadata = MetadataArtifactModel.query. \
            filter(MetadataArtifactModel.id == artifact_metadata_id). \
            first()
        if artifact_metadata is None:
            abort(404)

        if request_user.ancient_coin < artifact_metadata.cost:
            return {
                'success': False,
                'message': 'not enough ancient coin'
            }

        prev_show_window_item = ArtifactShowWindowModel.query. \
            filter(ArtifactShowWindowModel.user_id == request_user.id). \
            filter(ArtifactShowWindowModel.artifact_metadata_id == artifact_metadata_id). \
            first()
        if prev_show_window_item is None:
            abort(404)

        prev_show_window_item.visible = False

        request_user.ancient_coin -= artifact_metadata.cost

        new_artifact = ArtifactModel(user_id=request_user.id, artifact_metadata_id=artifact_metadata.id)
        db.session.add(new_artifact)

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'artifact_id': new_artifact.id,
            'ancient_coin': request_user.ancient_coin
        }
