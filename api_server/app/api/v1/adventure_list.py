from app import db, api_root, access_token_required
from app.util.get_adventure_random_list import get_adventure_random_list
from app.models.adventure import AdventureModel
from flask.ext.restful import Resource

"""
    # API : 모험 리스트
    # DESCRIPTION
        # 유저가 수행할 수 있는 모험 리스트를 반환
        # 등장조건에 부합하는 모험이 최대 슬롯 갯수만큼 등장
        # 현재 슬롯 갯수에 비해 등장하는 모험이 적다면 리스트 refresh 수행

"""


@api_root.resource('/v1/adventures')
class AdventureList(Resource):
    @access_token_required
    def get(self, request_user):
        # 1. 그 퀘스트의 최대레벨 ~ 최대 레벨 -3 사이에서 랜덤하게 등장한다
        # 2. 등장 조건 영웅이 있을 때 그 영웅의 이름을 가진
        # 3. 진행 되고 있는 모험은 무조건 있어야 한다

        adventures = AdventureModel.query.\
            filter(AdventureModel.user_id == request_user.id). \
            all()

        visible_adventure_count = 0

        for adventure in adventures:
            if adventure.visible:
                visible_adventure_count += 1

        # 유저 모험 슬롯보다 visible 모험이 적다면 시작한 모험 빼고, visible 을 False
        if visible_adventure_count < request_user.adventure_slot:
            for adventure in adventures:
                if not adventure.is_start:
                    adventure.visible = False
            # 모험 리스트를 초기화 시키는 유틸 함수
            random_adventure_list = get_adventure_random_list(adventures, request_user)
            for adventure in random_adventure_list:
                adventure.visible = True

        result = []
        for adventure in adventures:
            data = {
                'id': adventure.id,
                'adventure_metadata_id': adventure.adventure_metadata_id,
                'is_start': adventure.is_start,
                'hero_1_id': adventure.hero_1_id,
                'hero_2_id': adventure.hero_2_id,
                'hero_3_id': adventure.hero_3_id,
                'visible': adventure.visible,
                'max_level': adventure.max_level,
                'execution_count': adventure.execution_count
            }
            result.append(data)

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
