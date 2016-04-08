from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, FLOAT, ARRAY, BOOLEAN


class UserShortTermPropertyModel(db.Model):
    __tablename__ = 'user_short_term_properties'

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

    gold = db.Column(
        FLOAT,
        default=0
    )

    world = db.Column(
        INTEGER,
        default=0
    )

    stage = db.Column(
        INTEGER,
        default=0
    )

    accrue_stage = db.Column(
        INTEGER,
        default=0
    )

    quest = db.Column(
        ARRAY(INTEGER),
    )

    quest_level = db.Column(
        ARRAY(INTEGER),
    )

    quest_auto = db.Column(
        ARRAY(BOOLEAN),
    )

    quest_start_time = db.Column(
        ARRAY(db.String(64))
    )

    hero_party_stage = db.Column(
        ARRAY(INTEGER),
    )

    hero_level_stage = db.Column(
        ARRAY(INTEGER),
    )

    hero_party_dungeon = db.Column(
        ARRAY(INTEGER),
    )
