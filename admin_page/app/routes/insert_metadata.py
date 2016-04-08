import csv
from app import db, DATA_VERSION

from app.models.constants import ConstantsModel
from app.models.metadata.dungeon_achievements import MetadataDungeonAchievementModel
from app.models.metadata.hero import MetadataHeroModel
from app.models.metadata.equipment import MetadataEquipmentModel
from app.models.metadata.equipment_option import MetadataEquipmentOptionModel
from app.models.metadata.adventure import MetadataAdventureModel
from app.models.metadata.artifact import MetadataArtifactModel
from app.models.metadata.artifact_option import MetadataArtifactOptionModel
from app.models.metadata.lottery import MetadataLotteryModel
from app.models.metadata.reward import MetadataRewardModel
from app.models.metadata.cashshop import MetadataCashShopItemModel
from app.models.metadata.achievement import MetadataAchievementModel
from app.models.metadata.league import MetadataLeagueModel
from app.models.metadata.stage import MetadataStageModel


DIR_PATH = 'app/static/data/'
DATA_START_ROW_NUMBER = 2

hero_dict = [
    ['character_data.csv', 'string'],
    ['id', 'int'],
    ['name', 'string'],
    ['group', 'string'],
    ['area', 'string'],
    ['sex', 'string'],
    ['hero_class', 'string'],
    ['enchant_base_cost', 'int'],
    ['enchant_cost_increase_rate', 'float'],
    ['base_skill_upgrade_cost', 'int'],
    ['skill_upgrade_cost_increase_rate', 'float'],
    ['hire_cost', 'int'],
    ['grade', 'int'],
    ['is_basic_grade', 'bool'],
    ['is_evolve', 'bool'],
]


equipment_dict = [
    ['equipment_data.csv', 'string'],
    ['id', 'int'],
    ['name', 'string'],
    ['type', 'string'],
    ['grade', 'int'],
    ['basic_ability_value', 'float'],
    ['base_enchant_cost', 'float'],
    ['enchant_cost_rate', 'float'],
    ['enchant_ability_rate', 'float'],
    ['base_breakthrough_cost', 'float'],
    ['breakthrough_cost_step', 'float'],
    ['breakthrough_cost_limit', 'float'],
    ['breakthrough_point', 'int'],
    ['breakthrough_increase_by_enchant_level', 'float']
]


equipment_option_dict = [
    ['equipment_option_data.csv', 'string'],
    ['id', 'int'],
    ['equipment_metadata_id', 'int'],
    ['type', 'string'],
    ['min_value', 'float'],
    ['max_value', 'float'],
    ['base_unit', 'string']
]


adventure_dict = [
    ['adventure_data.csv', 'string'],
    ['id', 'int'],
    ['name', 'string'],
    ['level', 'int'],
    ['suitable_difficulty', 'int'],
    ['dispatch_number', 'int'],
    ['maximum_success_rate', 'float'],
    ['shortfall_penalty', 'float'],
    ['hero_name_for_appear', 'string'],
    ['appear_rate', 'float'],
    ['execution_limit', 'int'],
    ['trait_grade', 'int'],
    ['trait_grade_bonus', 'float'],
    ['trait_area', 'string'],
    ['trait_area_bonus', 'float'],
    ['trait_group', 'string'],
    ['trait_group_bonus', 'float'],
    ['trait_sex', 'string'],
    ['trait_sex_bonus', 'float'],
    ['trait_class', 'string'],
    ['trait_class_bonus', 'float'],
    ['run_duration', 'integer'],
    ['final_reward_name', 'string'],
    ['main_reward_name', 'string'],
    ['main_reward_name', 'string']
]


artifact_dict = [
    ['artifact_data.csv', 'string'],
    ['id', 'int'],
    ['name', 'string'],
    ['cost', 'int'],
    ['max_level', 'int'],
    ['upgrade_cost_increase_rate', 'float']
]


artifact_option_dict = [
    ['artifact_option_data.csv', 'string'],
    ['id', 'int'],
    ['artifact_metadata_id', 'int'],
    ['type', 'string'],
    ['base', 'float'],
    ['increase_per_level', 'float']
]


lottery_dict = [
    ['lottery_data.csv', 'string'],
    ['id', 'int'],
    ['group_id', 'int'],
    ['type', 'string'],
    ['target_metadata_id', 'int'],
    ['amount', 'int'],
    ['weight', 'int']
]


reward_dict = [
    ['reward_data.csv', 'string'],
    ['id', 'int'],
    ['name', 'string'],
    ['type', 'string'],
    ['target_metadata_id', 'int'],
    ['amount', 'int'],
]


cash_shop_dict = [
    ['cash_shop_data.csv', 'string'],
    ['id', 'int'],
    ['item_type', 'string'],
    ['item_group', 'string'],
    ['image_type', 'string'],
    ['image_src', 'string'],
    ['cost_type', 'string'],
    ['cost', 'int'],
    ['reward_name', 'string']
]


achievement_dict = [
    ['achievement_data.csv', 'string'],
    ['id', 'int'],
    ['name', 'string'],
    ['type', 'string'],
    ['value', 'int'],
    ['reward_name', 'string']
]


constants_dict = [
    ['constants_data.csv', 'string'],
    ['id', 'int'],
    ['key', 'string'],
    ['additional_key', 'string'],
    ['value', 'string'],
    ['value_type', 'string']
]


dungeon_achievement_dict = [
    ['dungeon_achievement_data.csv', 'string'],
    ['id', 'int'],
    ['type', 'string'],
    ['value', 'int'],
    ['reward_name', 'string'],
]

league_dict = [
    ['league_data.csv', 'string'],
    ['id', 'int'],
    ['name', 'string'],
    ['description', 'string'],
    ['status', 'string'],
    ['type', 'string'],
    ['num_of_party_member', 'int'],
    ['start_max_ticket', 'int'],
    ['end_max_ticket', 'int'],
    ['ticket_price', 'int'],
    ['increase_max_ticket_price', 'int'],
    ['increase_ticket_interval', 'int'],
    ['change_opponent_price', 'int'],
]

stage_dict = [
    ['stage_data.csv', 'string'],
    ['id', 'int'],
    ['world', 'int'],
    ['stage', 'int'],
    ['boss_reward', 'string[]'],
    ['first_reward', 'string[]'],
]


def db_insert(data_type, bucket_key, filename):
    # bucket에서 불러온다
    bucket_key.get_contents_to_filename(DIR_PATH + str(DATA_VERSION) + '/' + filename)
    if data_type == 'character':
        insert_metadata_hero()
    elif data_type == 'equipment':
        insert_metadata_equipment()
    elif data_type == 'equipment_option':
        insert_metadata_equipment_option()
    elif data_type == 'reward':
        insert_metadata_reward()
    elif data_type == 'lottery':
        insert_metadata_lottery()
    elif data_type == 'league':
        insert_metadata_league()
    elif data_type == 'cash_shop':
        insert_metadata_cash_shop()
    elif data_type == 'dungeon_achievement':
        insert_metadata_dungeon_achievement()
    elif data_type == 'adventure':
        insert_metadata_adventure()
    elif data_type == 'achievement':
        insert_metadata_achievement()
    elif data_type == 'artifact':
        insert_metadata_artifact()
    elif data_type == 'artifact_option':
        insert_metadata_artifact_option()
    elif data_type == 'constants':
        insert_metadata_constants()
    elif data_type == 'constants':
        insert_metadata_constants()
    elif data_type == 'stage':
        insert_metadata_stage()
    print('metadata db insert')



def get_value_by_type(data, value_set):
    value = data[value_set[0]]
    if value is not '' and value_set[1] == 'int':
        value = int(data[value_set[0]])
    elif value is not '' and value_set[1] == 'float':
        value = float(data[value_set[0]])
    elif value_set[1] == 'bool':
        if value == '':
            value = False
        else:
            value = bool(data[value_set[0]])
    elif value_set[1] == 'string[]':
        value = value.split('|')
    return value


def get_list_from_csv(file_name):
    csv_file = open(DIR_PATH + str(DATA_VERSION) + '/' + file_name, 'r', encoding='utf-8')
    reader = csv.reader(csv_file)

    entire_data = []
    for row in reader:
        entire_data.append(row)

    necessary_data = []
    for i in range(DATA_START_ROW_NUMBER, len(entire_data)):
        data = dict()
        for j in range(0, len(entire_data[i])):
            # ['column_name' : 'column data'] added
            data[entire_data[1][j]] = entire_data[i][j]
        necessary_data.append(data)
    csv_file.close()
    return necessary_data


def insert_metadata_hero():
    dictionary = hero_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        if data['area'] == 'enemy':
            continue
        metadata = MetadataHeroModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataHeroModel.query.\
            filter(MetadataHeroModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_adventure():
    query = "truncate table metadata_adventures cascade;"\
            "alter sequence metadata_adventures_id_seq restart 1;"
    db.session.execute(query)

    dictionary = adventure_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataAdventureModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataAdventureModel.query.\
            filter(MetadataAdventureModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_equipment():
    query = "truncate table metadata_equipments cascade;"\
            "alter sequence metadata_equipments_id_seq restart 1;"
    db.session.execute(query)

    dictionary = equipment_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataEquipmentModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataEquipmentModel.query.\
            filter(MetadataEquipmentModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_equipment_option():
    query = "truncate table metadata_equipment_options cascade;"\
            "alter sequence metadata_equipment_options_id_seq restart 1;"
    db.session.execute(query)

    dictionary = equipment_option_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataEquipmentOptionModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataEquipmentOptionModel.query.\
            filter(MetadataEquipmentOptionModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_artifact():
    query = "truncate table metadata_artifacts cascade;"\
            "alter sequence metadata_artifacts_id_seq restart 1;"
    db.session.execute(query)

    dictionary = artifact_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataArtifactModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataArtifactModel.query.\
            filter(MetadataArtifactModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_artifact_option():
    query = "truncate table metadata_artifact_options cascade;"\
            "alter sequence metadata_artifact_options_id_seq restart 1;"
    db.session.execute(query)
    dictionary = artifact_option_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataArtifactOptionModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataArtifactOptionModel.query.\
            filter(MetadataArtifactOptionModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_lottery():
    query = "truncate table metadata_lotteries cascade;"\
            "alter sequence metadata_lotteries_id_seq restart 1;"
    db.session.execute(query)
    dictionary = lottery_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataLotteryModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataLotteryModel.query.\
            filter(MetadataLotteryModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_reward():
    query = "truncate table metadata_rewards cascade;"\
            "alter sequence metadata_rewards_id_seq restart 1;"
    db.session.execute(query)

    dictionary = reward_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataRewardModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataRewardModel.query.\
            filter(MetadataRewardModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_cash_shop():
    query = "truncate table metadata_cash_shop_items cascade;"\
            "alter sequence metadata_cash_shop_items_id_seq restart 1;"
    db.session.execute(query)

    dictionary = cash_shop_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataCashShopItemModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataCashShopItemModel.query.\
            filter(MetadataCashShopItemModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_achievement():
    query = "truncate table metadata_achievements cascade;"\
            "alter sequence metadata_achievements_id_seq restart 1;"
    db.session.execute(query)

    dictionary = achievement_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataAchievementModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataAchievementModel.query.\
            filter(MetadataAchievementModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_constants():
    query = "truncate table constants cascade;"\
            "alter sequence constants_id_seq restart 1;"
    db.session.execute(query)

    dictionary = constants_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = ConstantsModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = ConstantsModel.query.\
            filter(ConstantsModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_dungeon_achievement():
    query = "truncate table metadata_dungeon_achievements cascade;"\
            "alter sequence metadata_dungeon_achievements_id_seq restart 1;"
    db.session.execute(query)

    dictionary = dungeon_achievement_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataDungeonAchievementModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataDungeonAchievementModel.query.\
            filter(MetadataDungeonAchievementModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_league():
    query = "truncate table metadata_leagues cascade;"\
            "alter sequence metadata_leagues_id_seq restart 1;"
    db.session.execute(query)

    dictionary = league_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataLeagueModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataLeagueModel.query.\
            filter(MetadataLeagueModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'


def insert_metadata_stage():
    query = "truncate table metadata_stages cascade;"\
            "alter sequence metadata_stages_id_seq restart 1;"
    db.session.execute(query)

    dictionary = stage_dict
    data_list = get_list_from_csv(dictionary[0][0])
    for data in data_list:
        metadata = MetadataStageModel()
        for i in range(1, len(dictionary)):
            insert_data = get_value_by_type(data, dictionary[i])
            if insert_data is not '':
                setattr(metadata, dictionary[i][0], insert_data)

        existing = MetadataStageModel.query.\
            filter(MetadataStageModel.id == metadata.id).\
            first()
        if existing:
            db.session.merge(metadata)
        else:
            db.session.add(metadata)
    db.session.commit()
    return 'success'
