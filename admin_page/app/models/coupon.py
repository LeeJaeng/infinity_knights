import datetime

from app import db
from sqlalchemy.dialects.postgres import BIGINT, INTEGER


class CouponModel(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    code = db.Column(
        db.String(64),
        nullable=False
    )

    reward_name = db.Column(
        db.String(64),
        nullable=False
    )

    stock = db.Column(
        INTEGER,
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



