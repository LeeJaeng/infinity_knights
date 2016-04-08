import datetime
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, BOOLEAN


class PurchaseVerificationModel(db.Model):
    __tablename__ = 'purchase_verification'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey("users.id"),
        nullable=False
    )

    developer_payload = db.Column(
        db.String(64),
    )

    is_verify = db.Column(
        BOOLEAN,
        default=False
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
