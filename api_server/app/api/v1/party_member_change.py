from app import api_root, db, access_token_required, get_constant_value, CONSTANTS_KEY_CHANGE_PARTY_MEMBER_COST
from flask.ext.restful import Resource

"""
    # API : 파티 멤버 변경
    # DESCRIPTION
        # 과금 재화인 gem을 이용하여 영웅 파티 변경

"""


@api_root.resource('/v1/party/change-member')
class PartyMemberChange(Resource):
    @access_token_required
    def get(self, request_user):
        if request_user.gem < get_constant_value(CONSTANTS_KEY_CHANGE_PARTY_MEMBER_COST):
            return {
                'success': False,
                'message': 'not enough gem'
            }

        request_user.gem -= get_constant_value(CONSTANTS_KEY_CHANGE_PARTY_MEMBER_COST)
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
        }
