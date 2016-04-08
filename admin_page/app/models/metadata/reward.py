from app import db
from sqlalchemy import Enum
from sqlalchemy.dialects.postgres import INTEGER


class MetadataRewardModel(db.Model):
    __tablename__ = 'metadata_rewards'

    id = db.Column(
        INTEGER,
        primary_key=True,
        index=True
    )

    name = db.Column(
        db.String(64),
        nullable=False
    )

    type = db.Column(
        db.String(64),
        nullable=False
    )

    target_metadata_id = db.Column(
        INTEGER,
        nullable=False
    )

    amount = db.Column(
        INTEGER,
        default=0
    )
