from app import db
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, ARRAY


class MetadataStageModel(db.Model):
    __tablename__ = 'metadata_stages'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    world = db.Column(
        INTEGER,
        nullable=False
    )

    stage = db.Column(
        INTEGER,
        nullable=False
    )

    boss_reward = db.Column(
        ARRAY(db.String(64)),
    )

    first_reward = db.Column(
        ARRAY(db.String(64)),
    )
