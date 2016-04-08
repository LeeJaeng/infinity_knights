from app import db
from sqlalchemy.dialects.postgres import BIGINT, INTEGER


class MetadataHonorShopModel(db.Model):
    __tablename__ = 'metadata_honor_shop_items'

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

    target_metadata_id = db.Column(
        INTEGER,
        nullable=False
    )

    amount = db.Column(
        INTEGER,
        nullable=False
    )

    cost = db.Column(
        INTEGER,
        nullable=False
    )
