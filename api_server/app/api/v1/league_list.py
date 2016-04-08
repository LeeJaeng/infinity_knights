from app import api_root, access_token_required

from app.models.league_user_property import LeagueUserPropertyModel
from app.models.metadata.league import MetadataLeagueModel
from flask.ext.restful import Resource
from sqlalchemy import and_

"""
    # API : 리그 리스트 조회
    # DESCRIPTION
        # 진행중인 리그 리스트 조회

"""


@api_root.resource('/v1/leagues')
class LeagueList(Resource):
    @access_token_required
    def get(self, request_user):
        league_metadata_list = MetadataLeagueModel.query. \
            outerjoin(LeagueUserPropertyModel,
                      and_(MetadataLeagueModel.id == LeagueUserPropertyModel.league_id,
                           LeagueUserPropertyModel.user_id == request_user.id)). \
            with_entities(MetadataLeagueModel.id,
                          MetadataLeagueModel.name,
                          MetadataLeagueModel.description,
                          MetadataLeagueModel.type,
                          LeagueUserPropertyModel.ticket,
                          LeagueUserPropertyModel.max_ticket). \
            filter(MetadataLeagueModel.status == 'ongoing'). \
            order_by(MetadataLeagueModel.id.asc()). \
            all()

        result = []
        for league_metadata in league_metadata_list:
            data = {
                'id': league_metadata.id,
                'name': league_metadata.name,
                'description': league_metadata.description,
                'type': str(league_metadata.type)
            }

            if league_metadata.ticket is not None:
                data['ticket'] = league_metadata.ticket
                data['max_ticket'] = league_metadata.max_ticket

            result.append(data)

        # TODO : marshalling
        return {
            'success': True,
            'result': result
        }
