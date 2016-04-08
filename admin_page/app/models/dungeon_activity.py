import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, BOOLEAN, ARRAY


class DungeonActivityModel(db.Model):
    __tablename__ = 'dungeon_activities'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey("users.id")
    )

    step = db.Column(
        INTEGER,
        default=1
    )

    enter = db.Column(
        INTEGER,
        default=0
    )

    ticket = db.Column(
        INTEGER,
        default=5
    )

    is_start = db.Column(
        BOOLEAN,
        default=False
    )

    achievement_list = db.Column(
        ARRAY(INTEGER),
        default=[]
    )

    max_ticket = db.Column(
        INTEGER,
        default=5
    )

    created_date = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow
    )

    updated_date = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
