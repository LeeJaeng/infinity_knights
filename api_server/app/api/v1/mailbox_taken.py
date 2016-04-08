from app import api_root, access_token_required, db
from app.models.mailbox import MailboxModel
from app.util.get_reward import get_reward
from flask.ext.restful import Resource, abort

"""
    # API : 메일 수령
    # DESCRIPTION
        # 나에게 온 메일 수령 (보상 수령)

"""


@api_root.resource('/v1/mailbox/<int:mail_id>/taken')
class MailboxTaken(Resource):
    @access_token_required
    def get(self, request_user, mail_id):
        mail = MailboxModel.query. \
            filter(MailboxModel.id == mail_id). \
            filter(MailboxModel.user_id == request_user.id). \
            filter(MailboxModel.deleted == False). \
            first()
        if mail is None:
            abort(404)

        if mail.reward_taken:
            return {
                'success': False,
                'message': 'already reward taken'
            }

        get_reward(request_user, mail.reward_name)

        mail.reward_taken = True

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True
        }
