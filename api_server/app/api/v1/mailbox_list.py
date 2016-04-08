from app import api_root, access_token_required
from app.models.mailbox import MailboxModel
from flask.ext.restful import Resource

"""
    # API : 메일 확인
    # DESCRIPTION
        # 나에게 온 메일 리스트를 확인

"""


@api_root.resource('/v1/mailbox')
class Mailbox(Resource):
    @access_token_required
    def get(self, request_user):
        mails = MailboxModel.query. \
            filter(MailboxModel.user_id == request_user.id). \
            filter(MailboxModel.deleted == False). \
            order_by(MailboxModel.created_date.desc()). \
            all()

        result = []
        for mail in mails:
            result.append({
                'id': mail.id,
                'title': mail.title,
                'content': mail.content,
                'reward_taken': mail.reward_taken,
                'image_type': mail.image_type,
                'image_src': mail.image_src,
                'reward_name': mail.reward_name,
                'created_date': str(mail.created_date)
            })

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
