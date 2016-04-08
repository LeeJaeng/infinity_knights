import datetime

from app import db
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.dialects.postgres import BIGINT, BOOLEAN


class MailboxModel(db.Model):
    __tablename__ = 'mailboxes'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey('users.id')
    )

    title = db.Column(
        db.String(128),
        nullable=False
    )

    content = db.Column(
        db.String(2048),
        nullable=False
    )

    deleted = db.Column(
        BOOLEAN,
        default=False
    )

    reward_taken = db.Column(
        BOOLEAN,
        default=False
    )

    image_type = db.Column(
        Enum('local', 'online', name='mailbox_item_image_types'),
        nullable=False
    )

    image_src = db.Column(
        db.String(256),
        nullable=False
    )

    reward_name = db.Column(
        db.String(64),
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
