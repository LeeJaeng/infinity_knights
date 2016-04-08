from app import db
from sqlalchemy.dialects.postgres import BIGINT, INTEGER


class MetadataAchievementModel(db.Model):
    __tablename__ = 'metadata_achievements'

    id = db.Column(
        BIGINT,
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

    value = db.Column(
        INTEGER,
        nullable=False
    )

    reward_name = db.Column(
        db.String(64),
        nullable=False
    )
