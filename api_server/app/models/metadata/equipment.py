from app import db
from sqlalchemy import Enum
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, FLOAT


class MetadataEquipmentModel(db.Model):
    __tablename__ = 'metadata_equipments'

    types_enum = ('weapon', 'accessory')

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
        Enum('weapon', 'accessory', name='equipment_types'),
        nullable=False
    )

    grade = db.Column(
        INTEGER,
        default=1,
        nullable=False
    )

    basic_ability_value = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    base_enchant_cost = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    enchant_cost_rate = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    enchant_ability_rate = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    base_breakthrough_cost = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    breakthrough_cost_step = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    breakthrough_cost_limit = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    breakthrough_point = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    breakthrough_increase_by_enchant_level = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

