from app import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgres import INTEGER


class MetadataDungeonAchievementModel(db.Model):
    __tablename__ = 'metadata_dungeon_achievements'

    id = db.Column(
        INTEGER,
        primary_key=True,
        index=True
    )

    type = db.Column(
        Enum('enter', 'step', name='dungeon_achievement_types'),
        nullable=False
    )

    value = db.Column(
        INTEGER,
        default=1
    )

    reward_name = db.Column(
        db.String(64),
        nullable=False
    )
