from app import db
from sqlalchemy import Enum
from sqlalchemy.dialects.postgres import INTEGER, FLOAT, BOOLEAN


class MetadataHeroModel(db.Model):
    __tablename__ = 'metadata_heroes'

    id = db.Column(
        INTEGER,
        primary_key=True,
        index=True
    )

    name = db.Column(
        db.String(64),
        nullable=False
    )

    group = db.Column(
        Enum('human', 'elf', 'orc', 'furry', name='hero_group'),
        nullable=False
    )

    area = db.Column(
        Enum('bastia', 'hellas', 'zin', 'grundal', name='hero_area'),
        nullable=False
    )

    sex = db.Column(
        Enum('male', 'female', name='hero_sex'),
        nullable=False
    )

    hero_class = db.Column(
        Enum('warrior', 'knight', 'swordman', 'lancer', 'mage', 'archer', 'priest', 'shaman', name='hero_class'),
        nullable=False
    )

    enchant_base_cost = db.Column(
        INTEGER,
        default=45
    )

    enchant_cost_increase_rate = db.Column(
        FLOAT,
        default=1.1
    )

    base_skill_upgrade_cost = db.Column(
        INTEGER,
        default=5
    )

    skill_upgrade_cost_increase_rate = db.Column(
        FLOAT,
        default=2.1
    )

    hire_cost = db.Column(
        INTEGER,
        default=0
    )

    grade = db.Column(
        INTEGER,
        default=1
    )

    is_basic_grade = db.Column(
        BOOLEAN,
        nullable=False
    )

    is_evolve = db.Column(
        BOOLEAN,
        nullable=False
    )
