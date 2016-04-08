from app import api_root, access_token_required
from app.util.get_adventure_random_list import get_adventure_random_list
from app.models.adventure import AdventureModel
from app import db
from flask.ext.restful import Resource, request, abort

"""
    # API : 모험 리스트 즉시 새로고침
    # DESCRIPTION
        # 과금 재화인 gem을 사용하여서 모험 리스트를 새로고침

"""


@api_root.resource('/v1/adventures/list-immediate-refresh')
class AdventureListImmediateRefresh(Resource):
    @access_token_required
    def get(self, request_user):
        if 'cost' not in request.args:
            abort(400)
        cost = int(request.args['cost'])

        if cost > request_user.gem:
            return {
                'success': False,
                'message': 'not enough gem'
            }

        adventures = AdventureModel.query.\
            filter(AdventureModel.user_id == request_user.id).\
            all()

        # 시작하지 않은 모험 visible False로 초기화
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
        request_user.gem -= cost
        db.session.commit()

        # TODO : marshalling
        return {
            'gem': request_user.gem,
            'success': True,
            'result': result
        }
