from app import api_root, access_token_required, db
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.user import UserModel
from flask.ext.restful import Resource, abort, request

"""
    # API : 리그 랭킹
    # DESCRIPTION
        # 해당 리그 랭킹
        # 100명 까지 + 자기 자신

"""
RANK = 100


@api_root.resource('/v1/leagues/<int:league_id>/rank')
class LeagueRank(Resource):
    @access_token_required
    def get(self, request_user, league_id):
        properties = LeagueUserPropertyModel.query.\
            with_entities(LeagueUserPropertyModel.elo, LeagueUserPropertyModel.user_id,
                          LeagueUserPropertyModel.win, LeagueUserPropertyModel.lose,
                          LeagueUserPropertyModel.draw).\
            filter(LeagueUserPropertyModel.league_id == league_id). \
            order_by(LeagueUserPropertyModel.elo.desc()).\
            all()

        top_ranker = []
        top_ranker_id = []
        my_rank = None
        is_my_id = False

        count = 0
        rank = 1
        prev_elo = 0

        for data in properties:
            count += 1
            if count != 1:
                if prev_elo != data.elo:
                    rank = count
            # Top ranker 정보들
            top_ranker.append({
                'user_id': data.user_id,
                'rank': rank,
                'elo': data.elo,
                'lose': data.lose,
                'win': data.win,
                'draw': data.draw,
            })
            top_ranker_id.append(data.user_id)

            # 내 랭크 정보
            if data.user_id == request_user.id:
                is_my_id = True
                my_rank = {
                    'nickname': request_user.nickname,
                    'elo': data.elo,
                    'lose': data.lose,
                    'win': data.win,
                    'draw': data.draw,
                    'rank': rank,
                    'user_id': data.user_id
                }

            prev_elo = data.elo
            if count == 100 and is_my_id:
                break

        users = UserModel.query. \
            with_entities(UserModel.nickname).\
            filter(UserModel.id.in_(top_ranker_id)).\
            all()

        i = 0
        for user in users:
            top_ranker[i]['nickname'] = user.nickname
            i += 1

        # TODO : marshalling
        return {
            'success': True,
            'top_ranker': top_ranker,
            'my_rank': my_rank
        }
