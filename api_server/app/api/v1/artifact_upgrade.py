from app import api_root, db, access_token_required
from app.models.artifact import ArtifactModel
from app.models.metadata.artifact import MetadataArtifactModel
from flask.ext.restful import Resource, abort

"""
    # API : 유물 업그레이드
    # DESCRIPTION
        # 해당하는 유물의 레벨 Upgrade

"""


@api_root.resource('/v1/artifacts/<int:artifact_id>/upgrade')
class ArtifactUpgrade(Resource):
    @access_token_required
    def get(self, request_user, artifact_id):
        artifact = ArtifactModel.query. \
            join(MetadataArtifactModel). \
            add_columns(MetadataArtifactModel.max_level,
                        MetadataArtifactModel.cost.label('upgrade_base_cost'),
                        MetadataArtifactModel.upgrade_cost_increase_rate). \
            filter(ArtifactModel.user_id == request_user.id). \
            filter(ArtifactModel.id == artifact_id). \
            first()
        if artifact is None:
            abort(404)

        if artifact.ArtifactModel.level >= artifact.max_level:
            return {
                'success': False,
                'message': 'this artifact is already max level'
            }

        cost = artifact.upgrade_base_cost * pow(artifact.upgrade_cost_increase_rate, artifact.ArtifactModel.level)
        if request_user.ancient_coin < cost:
            return {
                'success': False,
                'message': 'not enough ancient coin'
            }

        artifact.ArtifactModel.level += 1
        request_user.ancient_coin -= cost
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'artifact_id': artifact_id,
            'level': artifact.ArtifactModel.level,
            'ancient_coin': request_user.ancient_coin
        }
