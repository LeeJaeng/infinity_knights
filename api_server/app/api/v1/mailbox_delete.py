from app import api_root, access_token_required, db
from app.models.mailbox import MailboxModel
from flask.ext.restful import Resource, abort

"""
    # API : 메일 삭제
    # DESCRIPTION
        # 관리자로부터 온 메일 삭제
        # reward를 받았을 때만 삭제 가능

"""


@api_root.resource('/v1/mailbox/<int:mail_id>/delete')
class MailboxDelete(Resource):
    @access_token_required
    def get(self, request_user, mail_id):
        mail = MailboxModel.query. \
            filter(MailboxModel.id == mail_id). \
            filter(MailboxModel.user_id == request_user.id). \
            filter(MailboxModel.deleted == False). \
            first()
        if mail is None:
            abort(404)

        if not mail.reward_taken:
            return {
                'success': False,
                'message': 'reward not taken'
            }

        mail.deleted = True

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True
        }
