import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, ARRAY


class LeagueUserPropertyModel(db.Model):
    __tablename__ = 'league_user_properties'

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

    user_id = db.Column(
        BIGINT,
        ForeignKey("users.id"),
        nullable=False
    )

    elo = db.Column(
        INTEGER,
        default=1500
    )

    win = db.Column(
        INTEGER,
        default=0
    )

    lose = db.Column(
        INTEGER,
        default=0
    )

    draw = db.Column(
        INTEGER,
        default=0
    )

    ticket = db.Column(
        INTEGER,
        default=0
    )

    hero_party = db.Column(
        ARRAY(INTEGER),
    )

    max_ticket = db.Column(
        INTEGER,
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
