from app import api_root, access_token_required, db
from app.models.adventure import AdventureModel
from app.util.get_adventure_random_list import get_adventure_random_list
from flask.ext.restful import Resource

"""
    # API : 모험 리스트 새로고침
    # DESCRIPTION
        # 모험 리스트를 새로고침
        # 클라이언트에서 일정 시간이 지난 뒤에 호출할 수 있는 API

"""


@api_root.resource('/v1/adventures/list-refresh')
class AdventureListRefresh(Resource):
    @access_token_required
    def get(self, request_user):

        adventures = AdventureModel.query.\
            filter(AdventureModel.user_id == request_user.id).\
            all()

        for adventure in adventures:
            if not adventure.is_start:
                adventure.visible = False

        random_adventure_list = get_adventure_random_list(adventures, request_user)
        result = []
        for adventure in random_adventure_list:
            adventure.visible = True
            data = {
                'id': adventure.id,
                'adventure_metadata_id': adventure.adventure_metadata_id,
                'visible': adventure.visible,
                'execution_count': adventure.execution_count
            }
            result.append(data)
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
