import datetime
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgres import BIGINT, INTEGER, DOUBLE_PRECISION


class UserAchievementModel(db.Model):
    __tablename__ = 'user_achievements'

    id = db.Column(
        BIGINT,
        primary_key=True,
        index=True
    )

    user_id = db.Column(
        BIGINT,
        ForeignKey('users.id'),
        nullable=False
    )

    stage_world_1 = db.Column(
        INTEGER,
        default=0
    )

    stage_world_2 = db.Column(
        INTEGER,
        default=0
    )

    accrue_rune_stone = db.Column(
        DOUBLE_PRECISION,
        default=0
    )

    accrue_honor_coin = db.Column(
        INTEGER,
        default=0
    )

    accrue_ancient_coin = db.Column(
        INTEGER,
        default=0
    )

    accrue_rebirth = db.Column(
        INTEGER,
        default=0
    )

    accrue_breakthrough = db.Column(
        INTEGER,
        default=0
    )

    max_hero_level = db.Column(
        INTEGER,
        default=0
    )

    max_hero_enchant = db.Column(
        INTEGER,
        default=0
    )

    league_try = db.Column(
        INTEGER,
        default=0
    )

    league_win = db.Column(
        INTEGER,
        default=0
    )

    adventure_try = db.Column(
        INTEGER,
        default=0
    )

    adventure_success = db.Column(
        INTEGER,
        default=0
    )

    buy_goods_honor_shop = db.Column(
        INTEGER,
        default=0
    )

    buy_goods_cash_shop = db.Column(
        INTEGER,
        default=0
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

    def property_to_dict(self):
        result = dict()
        result['stage_world_1'] = self.stage_world_1
        result['stage_world_2'] = self.stage_world_2
        result['accrue_rune_stone'] = self.accrue_rune_stone
        result['accrue_honor_coin'] = self.accrue_honor_coin
        result['accrue_rebirth'] = self.accrue_rebirth
        result['accrue_breakthrough'] = self.accrue_breakthrough
        result['accrue_ancient_coin'] = self.accrue_ancient_coin
        result['max_hero_enchant'] = self.max_hero_enchant
        result['max_hero_level'] = self.max_hero_level
        result['league_win'] = self.league_win
        result['league_try'] = self.league_try
        result['adventure_success'] = self.adventure_success
        result['adventure_try'] = self.adventure_try
        result['buy_goods_cash_shop'] = self.buy_goods_cash_shop
        result['buy_goods_honor_shop'] = self.buy_goods_honor_shop
        return result

