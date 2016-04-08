from app import db
from sqlalchemy import Enum
from sqlalchemy.dialects.postgres import INTEGER


class MetadataCashShopItemModel(db.Model):
    __tablename__ = 'metadata_cash_shop_items'

    id = db.Column(
        INTEGER,
        primary_key=True,
        index=True
    )

    item_type = db.Column(
        Enum('continual', 'ad_continual', 'stepped', 'one', name='cash_shop_item_type'),
        nullable=False
    )

    item_group = db.Column(
        db.String(64),
        nullable=False
    )

    image_type = db.Column(
        Enum('local', 'online', name='cash_shop_item_image_types'),
        nullable=False
    )

    image_src = db.Column(
        db.String(256),
        nullable=False
    )

    cost_type = db.Column(
        Enum('gem', 'cash', 'ad',  name='cash_shop_cost_types'),
        nullable=False
    )

    cost = db.Column(
        INTEGER,
        default=0
    )

    reward_name = db.Column(
        db.String(64),
        nullable=False
    )
