from app import api_root, db, access_token_required
from app.models.metadata.league import MetadataLeagueModel
from flask.ext.restful import Resource, abort

"""
    # API : 리그 티켓 구매
    # DESCRIPTION
        # 과금 재화인 gem을 이용하여 리그 티켓 구매

"""


@api_root.resource('/v1/leagues/<int:league_id>/buy-ticket')
class LeagueBuyTicket(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        league_metadata = MetadataLeagueModel.query. \
            filter(MetadataLeagueModel.id == league_id). \
            first()
        if league_metadata is None:
            abort(404)

        if request_user.gem < league_metadata.ticket_price:
            return {
                'success': False,
                'message': 'not enough gem'
            }

        request_user.gem -= league_metadata.ticket_price
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'gem': request_user.gem
        }
