from app import db
from app.models.user import UserModel
from app.worker import william


@william.task
def add_soul_stone(user_id, x):
    user = UserModel.query.\
        filter(UserModel.id == user_id).\
        first()
    if user is None:
        return None

    user.soul_stone += x
    db.session.commit()

    return x
