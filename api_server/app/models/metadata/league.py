import datetime

from app import db
from sqlalchemy.dialects.postgres import INTEGER, ENUM


class MetadataLeagueModel(db.Model):
    __tablename__ = 'metadata_leagues'

    id = db.Column(
        INTEGER,
        primary_key=True,
        index=True
    )

    name = db.Column(
        db.String(64)
    )

    description = db.Column(
        db.String(2048)
    )

    status = db.Column(
        ENUM('ongoing', 'end', 'hidden', name='league_status')
    )

    type = db.Column(
        ENUM('duel', 'race', name='league_types'),
        default='duel'
    )

    num_of_party_member = db.Column(
        INTEGER,
        default=5
    )

    start_max_ticket = db.Column(
        INTEGER,
        default=0
    )

    end_max_ticket = db.Column(
        INTEGER,
        default=0
    )

    ticket_price = db.Column(
        INTEGER,
        default=0
    )

    increase_max_ticket_price = db.Column(
        INTEGER,
        default=0
    )

    increase_ticket_interval = db.Column(
        INTEGER,
        default=0
    )

    change_opponent_price = db.Column(
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
