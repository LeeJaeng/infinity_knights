from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import INTEGER, ENUM


class MetadataLeagueRestrictionModel(db.Model):
    __tablename__ = 'metadata_league_restrictions'

    id = db.Column(
        INTEGER,
        primary_key=True,
        index=True
    )

    metadata_league_id = db.Column(
        INTEGER,
        ForeignKey("metadata_leagues.id"),
        nullable=False
    )

    type = db.Column(
        ENUM('class', 'group', name='league_restriction_types'),
        nullable=False
    )

    value = db.Column(
        ENUM('human', 'elf', 'orc', 'furry',                                                # group
             'warrior', 'knight', 'spearman', 'archer', 'magician', 'shaman', 'priest',     # class
             name='league_restriction_values')
    )
