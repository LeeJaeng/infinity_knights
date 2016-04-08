from app import api_root, access_token_required, db
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.metadata.league import MetadataLeagueModel
from flask.ext.restful import Resource, abort, request

"""
    # API : 리그 결투 참가 파티 변경
    # DESCRIPTION
        # 리그 결투에 참가할 내 파티 멤버 변경

"""


@api_root.resource('/v1/leagues/duels/<int:league_id>/party-member-change')
class LeagueDuelPartyMemberChange(Resource):
    @access_token_required
    def post(self, request_user, league_id):
        if 'heroes' not in request.json:
            abort(400)

        league_metadata = MetadataLeagueModel.query. \
            filter(MetadataLeagueModel.id == league_id). \
            filter(MetadataLeagueModel.status == 'ongoing'). \
            filter(MetadataLeagueModel.type == 'duel'). \
            order_by(MetadataLeagueModel.id.desc()). \
            first()
        if league_metadata is None:
            abort(404)

        new_party_member_id_list = request.json['heroes']
        num_of_party_member = len(new_party_member_id_list)
        if num_of_party_member > league_metadata.num_of_party_member:
            abort(400)
        # TODO : Hero 검증?

        league_user_property = LeagueUserPropertyModel.query.\
            filter(LeagueUserPropertyModel.user_id == request_user.id).\
            filter(LeagueUserPropertyModel.league_id == league_id).\
            first()
        if league_user_property is None:
            abort(404)

        league_user_property.hero_party = new_party_member_id_list

        db.session.commit()

        # TODO : marshalling
        return {
            'success': True,
            'hero_list': league_user_property.hero_party
        }
