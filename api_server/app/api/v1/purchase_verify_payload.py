from app import api_root, access_token_required, db
from app.models.purchase_verification import PurchaseVerificationModel
from flask.ext.restful import Resource, request


@api_root.resource('/v1/purchase/verify-payload')
class PurchaseVerifyPayload(Resource):
    @access_token_required
    def get(self, request_user):
        if 'developer_payload' not in request.args:
            return {
                'success': False
            }
        purchase_verification = PurchaseVerificationModel.query.\
            filter(PurchaseVerificationModel.user_id == request_user.id).\
            first()
        if purchase_verification is None:
            return {
                'success': False
            }

        developer_payload = request.args['developer_payload']

        if purchase_verification.developer_payload == developer_payload:
            purchase_verification.is_verify = True

        db.session.commit()

        return {
            'success': purchase_verification.is_verify
        }
