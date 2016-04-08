from app import db
from sqlalchemy import Enum
from sqlalchemy.dialects.postgres import INTEGER


class MetadataLotteryModel(db.Model):
    __tablename__ = 'metadata_lotteries'

    id = db.Column(
        INTEGER,
        primary_key=True,
        index=True
    )

    group_id = db.Column(
        INTEGER
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

    weight = db.Column(
        INTEGER,
        default=0
    )
