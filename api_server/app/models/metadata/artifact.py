from app import db
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, FLOAT


class MetadataArtifactModel(db.Model):
    __tablename__ = 'metadata_artifacts'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    name = db.Column(
        db.String(64),
        nullable=False
    )

    cost = db.Column(
        INTEGER,
        default=0
    )

    max_level = db.Column(
        INTEGER,
        nullable=False
    )

    upgrade_cost_increase_rate = db.Column(
        FLOAT,
        default=1
    )
