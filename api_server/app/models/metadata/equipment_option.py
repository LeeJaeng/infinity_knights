from app import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, FLOAT, INTEGER


class MetadataEquipmentOptionModel(db.Model):
    __tablename__ = 'metadata_equipment_options'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    equipment_metadata_id = db.Column(
        INTEGER,
        ForeignKey('metadata_equipments.id')
    )

    type = db.Column(
        db.String(64),
        nullable=False
    )

    min_value = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    max_value = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )

    base_unit = db.Column(
        Enum('1', '0.1', name='base_unit'),
        nullable=False
    )
