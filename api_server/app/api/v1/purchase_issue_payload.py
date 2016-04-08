import uuid
from app import api_root, access_token_required, db
from app.models.purchase_verification import PurchaseVerificationModel
from flask.ext.restful import Resource


@api_root.resource('/v1/purchase/issue-payload')
class PurchaseIssuePayload(Resource):
    @access_token_required
    def get(self, request_user):

        purchase_verification = PurchaseVerificationModel.query.\
            filter(PurchaseVerificationModel.user_id == request_user.id).\
            first()
        if purchase_verification is None:
            return {
                'success': False
            }

        str_uuid = str(uuid.uuid4()).replace("-", "")
        developer_payload = "{0}_{1}".format(request_user.id, str_uuid)

        purchase_verification.developer_payload = developer_payload
        db.session.commit()

        return {
            'success': True,
            'developer_payload': developer_payload
        }
