import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, ENUM


class LeagueDuelHistoryModel(db.Model):
    __tablename__ = 'league_duel_histories'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    league_id = db.Column(
        INTEGER,
        ForeignKey("metadata_leagues.id"),
        nullable=False
    )

    user_id1 = db.Column(
        BIGINT,
        ForeignKey("users.id"),
        nullable=False
    )

    user_id2 = db.Column(
        BIGINT,
        ForeignKey("users.id"),
        nullable=False
    )

    state = db.Column(
        ENUM('win', 'lose', 'draw', 'ready', 'start', name='league_duel_history_states'),
        default='lose'
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
