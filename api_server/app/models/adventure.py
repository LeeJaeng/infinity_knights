import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, BOOLEAN

class AdventureModel(db.Model):
    __tablename__ = 'adventures'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey("users.id"),
        nullable=False
    )

    adventure_metadata_id = db.Column(
        INTEGER,
        ForeignKey("metadata_adventures.id")
    )

    execution_count = db.Column(
        INTEGER,
        default=0
    )

    is_start = db.Column(
        BOOLEAN,
        default=False
    )

    hero_1_id = db.Column(
        BIGINT,
        ForeignKey('heroes.id')
    )

    hero_2_id = db.Column(
        BIGINT,
        ForeignKey('heroes.id')
    )

    hero_3_id = db.Column(
        BIGINT,
        ForeignKey('heroes.id')
    )

    max_level = db.Column(
        INTEGER,
        default=1
    )

    duration_decrease_rate = db.Column(
        INTEGER,
        default=0
    )

    visible = db.Column(
        BOOLEAN,
        default=False
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
