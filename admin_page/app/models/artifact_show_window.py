import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, BOOLEAN


class ArtifactShowWindowModel(db.Model):
    __tablename__ = 'artifact_show_windows'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey('users.id')
    )

    artifact_metadata_id = db.Column(
        INTEGER,
        ForeignKey('metadata_artifacts.id'),
        nullable=False
    )

    visible = db.Column(
        BOOLEAN,
        default=True
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
