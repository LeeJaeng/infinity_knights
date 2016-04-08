from app import api_root, access_token_required, db
from app.models.league_duel_history import LeagueDuelHistoryModel
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.metadata.league import MetadataLeagueModel
from app.util.league import get_league_opponent
from flask.ext.restful import Resource, abort, request

"""
    # API : 리그 결투 등록
    # DESCRIPTION
        # 진행되는 리그에 영웅 파티를 가지고 등록
        # 리그 히스토리에 등록

"""


@api_root.resource('/v1/leagues/duels/<int:league_id>/register')
class LeagueDuelRegister(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        league_metadata = MetadataLeagueModel.query. \
            filter(MetadataLeagueModel.id == league_id). \
            filter(MetadataLeagueModel.status == 'ongoing'). \
            filter(MetadataLeagueModel.type == 'duel'). \
            order_by(MetadataLeagueModel.id.desc()). \
            first()
        if league_metadata is None:
            abort(404)

        league_user_property = LeagueUserPropertyModel.query. \
            filter(LeagueUserPropertyModel.league_id == league_id). \
            filter(LeagueUserPropertyModel.user_id == request_user.id). \
            first()
        if league_user_property is not None:
            abort(400)

        league_user_property = LeagueUserPropertyModel(league_id=league_id,
                                                       user_id=request_user.id,
                                                       max_ticket=league_metadata.start_max_ticket,
                                                       ticket=league_metadata.start_max_ticket)
        db.session.add(league_user_property)
        db.session.commit()

        # 1500점 시작
        opponent = get_league_opponent(league_user_property.elo, league_id, request_user)
        if opponent:
            new_history = LeagueDuelHistoryModel(league_id=league_id,
                                                 user_id1=request_user.id,
                                                 user_id2=opponent.user_id,
                                                 state='ready')
            db.session.add(new_history)
        db.session.commit()

        # TODO : marshalling
        return {
            'success': True
        }
