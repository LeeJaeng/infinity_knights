import datetime

from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER


class CouponHistoryModel(db.Model):
    __tablename__ = 'coupon_histories'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey('users.id')
    )

    coupon_id = db.Column(
        INTEGER,
        ForeignKey('coupons.id'),
        nullable=False
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

