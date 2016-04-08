from app import api_root, access_token_required
from app.models.artifact import ArtifactModel
from app.models.metadata.artifact_option import MetadataArtifactOptionModel
from flask.ext.restful import Resource

"""
    # API :  유물 리스트
    # DESCRIPTION
        # 유저가 소유한 유물과 옵션 리스트를 반환

"""


@api_root.resource('/v1/artifacts')
class ArtifactList(Resource):
    @access_token_required
    def get(self, request_user):
        artifacts = ArtifactModel.query. \
            filter(ArtifactModel.user_id == request_user.id). \
            all()

        artifact_metadata_id_list = [item.artifact_metadata_id for item in artifacts]
        artifact_option_metadata_list = MetadataArtifactOptionModel.query. \
            filter(MetadataArtifactOptionModel.artifact_metadata_id.in_(artifact_metadata_id_list)). \
            all()

        result = []
        for item in artifacts:
            elem = dict()
            elem['id'] = item.id
            elem['artifact_metadata_id'] = item.artifact_metadata_id
            elem['level'] = item.level
            elem['options'] = [option.id for option in artifact_option_metadata_list
                               if option.artifact_metadata_id == item.artifact_metadata_id]

            result.append(elem)

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
