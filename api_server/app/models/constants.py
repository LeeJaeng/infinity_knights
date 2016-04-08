from app import db
from sqlalchemy import Enum
from sqlalchemy.dialects.postgres import BIGINT, FLOAT, INTEGER


class ConstantsModel(db.Model):
    __tablename__ = 'constants'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    key = db.Column(
        db.String(64),
        nullable=False
    )

    additional_key = db.Column(
        db.String(64)
    )

    value_type = db.Column(
        Enum('int', 'float', 'bool', 'string', name='constants_value_type'),
        nullable=False
    )

    value = db.Column(
        db.String(64),
        nullable=False
    )
