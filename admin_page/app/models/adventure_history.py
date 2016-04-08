import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, BOOLEAN


class AdventureHistoryModel(db.Model):
    __tablename__ = 'adventure_histories'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey("users.id")
    )

    adventure_metadata_id = db.Column(
        INTEGER,
        ForeignKey("metadata_adventures.id"),
        nullable=False
    )

    hero_1_id = db.Column(
        BIGINT,
        ForeignKey("heroes.id")
    )

    hero_2_id = db.Column(
        BIGINT,
        ForeignKey("heroes.id")
    )

    hero_3_id = db.Column(
        BIGINT,
        ForeignKey("heroes.id")
    )

    is_complete = db.Column(
        BOOLEAN,
        nullable=False
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
