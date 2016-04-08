from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, FLOAT


class EquipmentOptionModel(db.Model):
    __tablename__ = 'equipment_options'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    equipment_id = db.Column(
        BIGINT,
        ForeignKey("equipments.id")
    )

    option_metadata_id = db.Column(
        INTEGER,
        ForeignKey("metadata_equipment_options.id"),
        nullable=False
    )

    value = db.Column(
        FLOAT,
        default=0,
        nullable=False
    )
