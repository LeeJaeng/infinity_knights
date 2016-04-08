from app import db
from app.models.dungeon_activity import DungeonActivityModel
from app.worker import william


@william.task
def increase_dungeon_ticket(user_id):
    activity = DungeonActivityModel.query.\
        filter(DungeonActivityModel.user_id == user_id).\
        first()
    if activity is None:
        return None

    activity.ticket = (activity.ticket + 1) % activity.max_ticket
    db.session.commit()

    return activity.ticket
