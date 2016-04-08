import datetime
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import INTEGER, BIGINT


class CashShopHistoryModel(db.Model):
    __tablename__ = 'cash_shop_histories'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey('users.id')
    )

    item_id = db.Column(
        INTEGER,
        ForeignKey('metadata_cash_shop_items.id')
    )

    created_date = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow
    )
