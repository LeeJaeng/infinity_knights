from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, FLOAT


class MetadataArtifactOptionModel(db.Model):
    __tablename__ = 'metadata_artifact_options'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    artifact_metadata_id = db.Column(
        INTEGER,
        ForeignKey('metadata_artifacts.id'),
        nullable=False
    )

    type = db.Column(
        db.String(64),
        nullable=False
    )

    base = db.Column(
        FLOAT,
        default=0
    )

    increase_per_level = db.Column(
        FLOAT,
        default=0
    )
