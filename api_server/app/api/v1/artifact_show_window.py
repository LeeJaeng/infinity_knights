from app import api_root, access_token_required
from app.models.artifact_show_window import ArtifactShowWindowModel
from flask.ext.restful import Resource

"""
    # API : 유물 쇼윈도우
    # DESCRIPTION
        # 구매 가능한 유물 리스트를 쇼 윈도우 형식으로 반환

"""


@api_root.resource('/v1/artifacts/show-window')
class ArtifactShowWindow(Resource):
    @access_token_required
    def get(self, request_user):
        artifact_show_window_list = ArtifactShowWindowModel.query. \
            filter(ArtifactShowWindowModel.user_id == request_user.id). \
            all()

        result = [item.artifact_metadata_id for item in artifact_show_window_list if item.visible]

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
