from app import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, FLOAT, INTEGER


class MetadataAdventureModel(db.Model):
    __tablename__ = 'metadata_adventures'

    # https://docs.google.com/spreadsheets/d/1CSMfyE1UVuxOahIFFK213OjbxUqTtYmBTyZPdO9SRXA/edit#gid=1529864724
    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    name = db.Column(
        db.String(64),
        nullable=False
    )

    level = db.Column(
        INTEGER,
        nullable=False
    )

    suitable_difficulty = db.Column(
        INTEGER,
        nullable=False
    )

    dispatch_number = db.Column(
        INTEGER,
        nullable=False
    )

    maximum_success_rate = db.Column(
        FLOAT,
        nullable=False
    )

    shortfall_penalty = db.Column(
        FLOAT,
        nullable=False
    )

    hero_name_for_appear = db.Column(
        db.String(64)
    )

    appear_rate = db.Column(
        FLOAT,
        nullable=False
    )

    execution_limit = db.Column(
        INTEGER,
        nullable=False
    )

    trait_grade = db.Column(
        INTEGER
    )

    trait_grade_bonus = db.Column(
        FLOAT
    )

    trait_area = db.Column(
        Enum('bastia', 'hellas', 'zin', 'grundal', name='trait_area')
    )

    trait_area_bonus = db.Column(
        FLOAT
    )

    trait_group = db.Column(
        Enum('human', 'elf', 'orc', 'furry', name='trait_group')
    )

    trait_group_bonus = db.Column(
        FLOAT
    )

    trait_sex = db.Column(
        Enum('male', 'female', name='trait_sex')
    )

    trait_sex_bonus = db.Column(
        FLOAT
    )

    trait_class = db.Column(
        Enum('warrior', 'knight', 'swordman', 'lancer', 'mage', 'archer', 'priest', 'shaman', name='trait_class')
    )

    trait_class_bonus = db.Column(
        FLOAT
    )

    run_duration = db.Column(
        INTEGER,
        nullable=False
    )

    final_reward_name = db.Column(
        db.String(64),
    )

    main_reward_name = db.Column(
        db.String(64),
        nullable=False
    )

    additional_reward_name = db.Column(
        db.String(64)
    )


