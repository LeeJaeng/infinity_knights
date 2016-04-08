from app import db
from app.models.league_user_property import LeagueUserPropertyModel
from app.worker import william


@william.task
def increase_league_ticket(league_id, user_id):
    user_property = LeagueUserPropertyModel.query. \
        filter(LeagueUserPropertyModel.league_id == league_id). \
        filter(LeagueUserPropertyModel.user_id == user_id). \
        first()
    if user_property is None:
        return None

    user_property.ticket = (user_property.ticket + 1) % user_property.max_ticket
    db.session.commit()

    return user_property.ticket
