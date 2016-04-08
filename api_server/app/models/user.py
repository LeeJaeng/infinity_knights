import datetime
import uuid

from app import db
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, UUID, DOUBLE_PRECISION


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    uuid = db.Column(
        UUID(as_uuid=True),
        nullable=False
    )

    access_token = db.Column(
        UUID(as_uuid=True)
    )

    nickname = db.Column(
        db.String(64),
    )

    time_gap = db.Column(
        INTEGER,
        default=0
    )

    rune_stone = db.Column(
        DOUBLE_PRECISION,
        default=0
    )

    group_soul_stone_human = db.Column(
        INTEGER,
        default=0
    )

    group_soul_stone_elf = db.Column(
        INTEGER,
        default=0
    )

    group_soul_stone_orc = db.Column(
        INTEGER,
        default=0
    )

    group_soul_stone_furry = db.Column(
        INTEGER,
        default=0
    )

    gem = db.Column(
        INTEGER,
        default=0
    )

    ancient_coin = db.Column(
        INTEGER,
        default=0
    )

    honor_coin = db.Column(
        INTEGER,
        default=0
    )

    adventure_slot = db.Column(
        INTEGER,
        default=2
    )

    last_elite_killed_date = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow
    )

    last_artifact_show_window_updated_date = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow
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

    def __init__(self):
        self.uuid = uuid.uuid4()
