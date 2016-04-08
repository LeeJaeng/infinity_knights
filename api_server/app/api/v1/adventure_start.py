from app import api_root, db, access_token_required
from app.models.adventure import AdventureModel
from app.util.adventure_exeuction_refresh import adventure_execution_refresh
from app.util.set_user_achievement_value import accrue_user_achievement_value
from app.models.metadata.adventure import MetadataAdventureModel
from flask.ext.restful import Resource, request, abort

"""
    # API : 모험 시작
    # DESCRIPTION
        # 유저가 보내준 영웅 파티를 이용하여 모험을 시작
        # 하루가 지났는지 확인하는 유틸 함수 사용해서 실행 횟수 새로고침
        # 모험 시작 업적 추가

"""


@api_root.resource('/v1/adventures/start')
class AdventureStart(Resource):
    @access_token_required
    def post(self, request_user):
        if 'heroes' not in request.json:
            abort(400)
        if 'adventure_id' not in request.json:
            abort(400)

        heroes = request.json['heroes']
        adventure_id = request.json['adventure_id']

        start_adventure = AdventureModel.query.\
            filter(AdventureModel.id == adventure_id).\
            first()
        if start_adventure is None:
            abort(400)
        metadata_adventure = MetadataAdventureModel.query.\
            filter(MetadataAdventureModel.id == start_adventure.adventure_metadata_id).\
            first()
        if metadata_adventure is None:
            abort(400)

        if len(heroes) > metadata_adventure.dispatch_number:
            return {
                'success': False,
                'message': 'too many heroes'
            }

        if start_adventure.is_start:
            return {
                'success': False,
                'message': 'already started'
            }

        adventures = AdventureModel.query.\
            filter(AdventureModel.user_id == request_user.id).\
            all()

        # 하루가 지난 지 확인하는 유틸함수
        adventure_execution_refresh(adventures, request_user)

        # checking execution limit
        if start_adventure.execution_count >= metadata_adventure.execution_limit:
            return {
                'success': False,
                'message': 'execution limit'
            }

        for i in range(0, len(heroes)):
            setattr(start_adventure, "hero_{}_id".format(i+1), heroes[i])

        start_adventure.execution_count += 1
        start_adventure.is_start = True
        # 모험 시작 횟수 업적에 추가
        accrue_user_achievement_value(request_user, 'adventure_try', 1)

        db.session.commit()

        return {
            'success': True,
            'adventure_id': adventure_id,
            'execution_count': start_adventure.execution_count
        }
