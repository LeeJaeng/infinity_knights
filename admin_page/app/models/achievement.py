import datetime
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER


class AchievementModel(db.Model):
    __tablename__ = 'achievements'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey('users.id'),
        nullable=False
    )

    achievement_metadata_id = db.Column(
        INTEGER,
        ForeignKey("metadata_achievements.id")
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

