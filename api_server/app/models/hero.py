import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, BOOLEAN


class HeroModel(db.Model):
    __tablename__ = 'heroes'

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

    hero_metadata_id = db.Column(
        INTEGER,
        ForeignKey("metadata_heroes.id")
    )

    enchant_level = db.Column(
        INTEGER,
        default=0
    )

    soul_stone = db.Column(
        INTEGER,
        default=0
    )

    skill_1_level = db.Column(
        INTEGER,
        default=1
    )

    skill_2_level = db.Column(
        INTEGER,
        default=1
    )

    skill_3_level = db.Column(
        INTEGER,
        default=1
    )

    equipment_id_weapon = db.Column(
        BIGINT,
        ForeignKey("equipments.id")
    )

    equipment_id_accessory = db.Column(
        BIGINT,
        ForeignKey("equipments.id")
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
