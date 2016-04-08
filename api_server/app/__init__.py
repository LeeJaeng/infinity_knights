import os
import uuid
from functools import wraps

from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['CONFIG_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')
app.config.from_pyfile(os.path.join(app.config.get('CONFIG_DIR'), 'secret.cfg'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]

if os.environ["STATE"] == 'development':
    app.debug = True
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy(app)

from app.models import *

db.create_all()

# metadata_version
DATA_VERSION = 1

def access_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'AccessToken' not in request.headers:
            abort(401)

        access_token = request.headers['AccessToken']

        try:
            uuid.UUID(access_token, version=4)
        except ValueError:
            abort(400)

        request_user = user.UserModel.query.\
            filter(user.UserModel.access_token == access_token).\
            first()
        if request_user is None:
            abort(404)

        kwargs['request_user'] = request_user
        return f(*args, **kwargs)
    return decorated_function


# global variables for game designer
CONSTANTS_KEY_SKILL_UPGRADE_COST_BASE = 'skill_upgrade_cost_base'
CONSTANTS_KEY_SKILL_UPGRADE_COST_FACTOR = 'skill_upgrade_cost_factor'
CONSTANTS_KEY_EVOLVE_SKILL_UPGRADE_COST_BASE = 'evolve_skill_upgrade_cost_base'
CONSTANTS_KEY_EVOLVE_SKILL_UPGRADE_COST_FACTOR = 'evolve_skill_upgrade_cost_factor'
CONSTANTS_KEY_EVOLVE_GEM_PRICE = 'evolve_gem_price'
CONSTANTS_KEY_MIN_TIME_CLEAR_ENEMY = 'min_time_clear_enemy'
CONSTANTS_KEY_CHANGE_PARTY_MEMBER_COST = 'change_party_member_cost'
CONSTANTS_KEY_DUNGEON_RESTRICTION = 'dungeon_restriction'
CONSTANTS_KEY_DUNGEON_MAX_TICKET = 'dungeon_max_ticket'
CONSTANTS_KEY_DUNGEON_MAX_TICKET_INCREASE_PRICE = 'dungeon_max_ticket_increase_price'
CONSTANTS_KEY_DUNGEON_TICKET_INCREASE_INTERVAL_IN_SECONDS = 'dungeon_ticket_increase_interval'
CONSTANTS_KEY_DUNGEON_REWARD_BASE = 'dungeon_reward_base'
CONSTANTS_KEY_DUNGEON_REWARD_INCREASE_FACTOR = 'dungeon_reward_increase_factor'
CONSTANTS_KEY_DUNGEON_TICKET_PRICE = 'dungeon_ticket_price'
CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_REFRESH_INTERVAL = 'artifact_show_window_refresh_interval'
CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_REFRESH_COST = 'artifact_show_window_refresh_cost'
CONSTANTS_KEY_ARTIFACT_SHOW_WINDOW_SIZE = 'artifact_show_window_size'
CONSTANTS_KEY_HERO_MAX_GRADE= 'hero_max_grade'
CONSTANTS_KEY_HERO_PROMOTE_PRICE = 'hero_promote_price'
CONSTANTS_KEY_DEFAULT_HERO_METADATA_ID = 'default_hero_metadata_id'
CONSTANTS_KEY_HERO_SOUL_STONE_BY_GRADE = 'hero_soul_stone_by_grade'
CONSTANTS_KEY_POWER_REVIVAL_GEM_COST = 'power_revival_gem_cost'
CONSTANTS_KEY_ADVENTURE_MAX_SLOT = 'adventure_max_slot'
CONSTANTS_KEY_ADVENTURE_MAX_DISPATCH_NUM = 'adventure_max_dispatch_num'
CONSTANTS_KEY_CLASS_BASIC_WEAPON_ID = 'class_basic_weapon_id'
CONSTANTS_KEY_CLASS_BASIC_ACCESSORY_ID = 'class_basic_accessory_id'
CONSTANTS_KEY_BREAKTHROUGH_ENCHANT_LEVEL_INCREASE = 'breakthrough_enchant_level_increase'


from app.models.constants import ConstantsModel


def get_constant_value(key, additional_key=None):
    constant_list = ConstantsModel.query.all()
    for constant in constant_list:
        if additional_key:
            if constant.key == key and constant.additional_key == str(additional_key):
                if constant.value_type == 'int':
                    return int(constant.value)
                elif constant.value_type == 'float':
                    return float(constant.value)
                elif constant.value_type == 'string':
                    return constant.value
                elif constant.value_type == 'bool':
                    return bool(constant.value)
        else:
            if constant.key == key:
                if constant.value_type == 'int':
                    return int(constant.value)
                elif constant.value_type == 'float':
                    return float(constant.value)
                elif constant.value_type == 'string':
                    return constant.value
                elif constant.value_type == 'bool':
                    return bool(constant.value)


from flask_restful import Api
api_root = Api(app, catch_all_404s=True)

from app.api.v1 import *
