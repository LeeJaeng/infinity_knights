import datetime
import random

from app import api_root, db, access_token_required, get_constant_value, \
    CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_REFRESH_INTERVAL, CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_REFRESH_COST
from app.models.artifact import ArtifactModel
from app.models.artifact_show_window import ArtifactShowWindowModel
from app.models.metadata.artifact import MetadataArtifactModel
from flask.ext.restful import Resource

"""
    # API : 유물 쇼 윈도우 새로고침
    # DESCRIPTION
        # 클라이언트에서 일정 시간이 지나야 호출 할 수 있는 API
        # 살 수 있는 유물 리스트를 새로고침

"""


@api_root.resource('/v1/artifacts/show-window-refresh')
class ArtifactShowWindowRefresh(Resource):
    @access_token_required
    def get(self, request_user):
        time_diff = datetime.datetime.utcnow() - request_user.last_artifact_show_window_updated_date
        if time_diff.total_seconds() < get_constant_value(CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_REFRESH_INTERVAL):
            if request_user.gem < get_constant_value(CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_REFRESH_COST):
                return {
                    'success': False,
                    'message': 'not enough gem'
                }
            request_user.gem -= get_constant_value(CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_REFRESH_COST)

        my_artifacts = ArtifactModel.query. \
            filter(ArtifactModel.user_id == request_user.id). \
            all()
        my_artifact_metadata_id_list = [item.artifact_metadata_id for item in my_artifacts]

        remain_artifact_metadata_list = MetadataArtifactModel.query .\
            filter(MetadataArtifactModel.id.notin_(my_artifact_metadata_id_list)). \
            all()
        remain_artifact_metadata_id_list = [item.id for item in remain_artifact_metadata_list]

        prev_artifact_show_window_list = ArtifactShowWindowModel.query. \
            filter(ArtifactShowWindowModel.user_id == request_user.id). \
            all()
        for prev_item in prev_artifact_show_window_list:
            prev_item.visible = True
            if len(remain_artifact_metadata_id_list) == 0:
                prev_item.visible = False
                continue

            artifact_metadata_id = random.choice(remain_artifact_metadata_id_list)
            remain_artifact_metadata_id_list.remove(artifact_metadata_id)

            prev_item.artifact_metadata_id = artifact_metadata_id

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'gem': request_user.gem
        }
