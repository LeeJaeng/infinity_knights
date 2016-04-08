import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, FLOAT


class EquipmentModel(db.Model):
    __tablename__ = 'equipments'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey("users.id")
    )

    hero_id = db.Column(
        BIGINT,
        ForeignKey("heroes.id")
    )

    equipment_metadata_id = db.Column(
        INTEGER,
        ForeignKey("metadata_equipments.id"),
        nullable=False
    )

    enchant_level = db.Column(
        INTEGER,
        default=0
    )

    enchant_level_limit = db.Column(
        INTEGER,
        default=9
    )

    curr_breakthrough_point = db.Column(
        FLOAT,
        default=0
    )

    next_breakthrough_cost = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    basic_ability = db.Column(
        FLOAT,
        default=0
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
