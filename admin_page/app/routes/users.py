from math import ceil
from app import app, db
from app.models.user import UserModel
from flask import render_template, request, redirect
from app.models.achievement import AchievementModel
from app.models.adventure_history import AdventureHistoryModel
from app.models.adventure import AdventureModel
from app.models.artifact_show_window import ArtifactShowWindowModel
from app.models.artifact import ArtifactModel
from app.models.coupon_history import CouponHistoryModel
from app.models.dungeon_activity import DungeonActivityModel
from app.models.equipment import EquipmentModel
from app.models.equipment_option import EquipmentOptionModel
from app.models.hero import HeroModel
from app.models.league_user_property import LeagueUserPropertyModel
from app.models.league_duel_history import LeagueDuelHistoryModel
from app.models.mailbox import MailboxModel
from app.models.purchase_verification import PurchaseVerificationModel
from app.models.user_achievement import UserAchievementModel
from app.models.user_short_term_property import UserShortTermPropertyModel
from app.models.cash_shop_history import CashShopHistoryModel
from sqlalchemy import or_



"""
    # ROUTE : users.py
    # DESCRIPTION
        # 관리자 페이지에서 유저 관리 부분 Route
        # User 목록 페이지에 사용될 Pagination 클래스 포함
        # 유저 Property edit
        # FOR TEST : 전 유저를 한 번에 삭제 할 수 있도록

"""


class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.list_num = 10

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def list_first_page(self):
        return (self.page // (self.list_num)) * self.list_num

    @property
    def list_last_page(self):
        last_page = (self.page // self.list_num) * self.list_num + self.list_num
        if last_page > self.pages:
            last_page = self.pages
        return last_page

    @property
    def last_object_index(self):
        last_index = self.page * self.per_page
        if last_index > self.total_count:
            last_index = self.total_count
        return last_index

    @property
    def first_object_index(self):
        first_index = (self.page-1) * self.per_page
        return first_index

    @property
    def next_list(self):
        next_list = self.list_last_page + 1
        if self.list_last_page == self.pages:
            next_list = self.list_last_page
        return next_list

    @property
    def prev_list(self):
        prev_list = self.list_first_page - 1
        if prev_list < 1:
            prev_list = 1
        return prev_list


@app.route('/admin/user')
def users():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    users = UserModel.query.order_by(UserModel.id.asc()).\
        all()
    PER_PAGE = 10
    total_count = len(users)

    pagination = Pagination(page, PER_PAGE, total_count)

    # TODO : delete at release
    print("pages: " + str(pagination.pages))
    print("list_first_page: " + str(pagination.list_first_page))
    print("list_last_page: " + str(pagination.list_last_page))
    print("first_object_index: " + str(pagination.first_object_index))
    print("last_object_index: " + str(pagination.last_object_index))
    print("prev_list: " + str(pagination.prev_list))
    print("next_list: " + str(pagination.next_list))

    # TODO : user_num은 나중에 빼야됨
    all_users = UserModel.query.count()
    return render_template('user.html', users=users, pagination=pagination, user_num=all_users)


@app.route('/admin/user/edit', methods=['POST'])
def edit_user_properties():
    user_properties = request.get_json()

    nickname = user_properties['nickname']
    user_id = user_properties['user_id']
    rune = user_properties['rune_stone']
    gem = user_properties['gem']
    ancient_coin = user_properties['ancient_coin']
    honor_coin = user_properties['honor_coin']
    group_soul_stone_human = user_properties['group_soul_stone_human']
    group_soul_stone_elf = user_properties['group_soul_stone_elf']
    group_soul_stone_orc = user_properties['group_soul_stone_orc']
    group_soul_stone_furry = user_properties['group_soul_stone_furry']
    adventure_slot = user_properties['adventure_slot']

    user = UserModel.query.\
        filter(UserModel.id == user_id).\
        first()

    user.nickname = nickname
    user.rune_stone = rune
    user.gem = gem
    user.ancient_coin = ancient_coin
    user.honor_coin = honor_coin
    user.group_soul_stone_human = group_soul_stone_human
    user.group_soul_stone_elf = group_soul_stone_elf
    user.group_soul_stone_orc = group_soul_stone_orc
    user.group_soul_stone_furry = group_soul_stone_furry
    user.adventure_slot = adventure_slot
    db.session.commit()

    return 'success'

@app.route('/admin/user/delete')
def delete_user():
    print("delete");

    user_id = request.args['id']
    achievements = AchievementModel.query.\
        filter(AchievementModel.user_id == user_id).\
        all()
    if achievements:
        for data in achievements:
            db.session.delete(data)

    adventure_histories = AdventureHistoryModel.query.\
        filter(AdventureHistoryModel.user_id == user_id).\
        all()
    if adventure_histories:
        for data in adventure_histories:
            db.session.delete(data)

    adventures = AdventureModel.query.\
        filter(AdventureModel.user_id == user_id).\
        all()
    if adventures:
        for data in adventures:
            db.session.delete(data)

    artifact_show_window = ArtifactShowWindowModel.query.\
        filter(ArtifactShowWindowModel.user_id == user_id).\
        all()
    if artifact_show_window:
        for data in artifact_show_window:
            db.session.delete(data)

    artifacts = ArtifactModel.query.\
        filter(ArtifactModel.user_id == user_id).\
        all()
    if artifacts:
        for data in artifacts:
            db.session.delete(data)

    coupon_histories = CouponHistoryModel.query.\
        filter(CouponHistoryModel.user_id == user_id).\
        all()
    if coupon_histories:
        for data in coupon_histories:
            db.session.delete(data)

    artifacts = ArtifactModel.query.\
        filter(ArtifactModel.user_id == user_id).\
        all()
    if artifacts:
        for data in artifacts:
            db.session.delete(data)

    dungeon_activity = DungeonActivityModel.query.\
        filter(DungeonActivityModel.user_id == user_id).\
        all()
    if dungeon_activity:
        for data in dungeon_activity:
            db.session.delete(data)

    heroes = HeroModel.query.\
        filter(HeroModel.user_id == user_id).\
        all()
    if heroes:
        for data in heroes:
            data.equipment_id_weapon = None
            data.equipment_id_accessory = None

    equipments = EquipmentModel.query.\
        filter(EquipmentModel.user_id == user_id).\
        all()
    if equipments:
        for equipment in equipments:
            equipment_options = EquipmentOptionModel.query. \
                filter(EquipmentOptionModel.equipment_id == equipment.id). \
                all()
            if equipment_options:
                for option in equipment_options:
                    db.session.delete(option)
                    db.session.commit()
            db.session.delete(equipment)

    league_user_property = LeagueUserPropertyModel.query.\
        filter(LeagueUserPropertyModel.user_id == user_id).\
        all()
    if league_user_property:
        for data in league_user_property:
            db.session.delete(data)

    league_history = LeagueDuelHistoryModel.query.\
        filter(or_(LeagueDuelHistoryModel.user_id1 == user_id, LeagueDuelHistoryModel.user_id2 == user_id)). \
        all()
    if league_history:
        for data in league_history:
            print(data.state)
            db.session.delete(data)

    mailbox = MailboxModel.query.\
        filter(MailboxModel.user_id == user_id).\
        all()
    if mailbox:
        for data in mailbox:
            db.session.delete(data)

    purchase_verification = PurchaseVerificationModel.query.\
        filter(PurchaseVerificationModel.user_id == user_id).\
        all()
    if purchase_verification:
        for data in purchase_verification:
            db.session.delete(data)

    user_achievement = UserAchievementModel.query.\
        filter(UserAchievementModel.user_id == user_id).\
        all()
    if user_achievement:
        for data in user_achievement:
            db.session.delete(data)

    user_shortterm = UserShortTermPropertyModel.query.\
        filter(UserShortTermPropertyModel.user_id == user_id).\
        all()
    if user_shortterm:
        for data in user_shortterm:
            db.session.delete(data)

    if heroes:
        for data in heroes:
            db.session.delete(data)

    cashshop = CashShopHistoryModel.query.\
        filter(CashShopHistoryModel.user_id == user_id).\
        all()
    if cashshop:
        for data in cashshop:
            db.session.delete(data)

    user = UserModel.query.\
        filter(UserModel.id == user_id).\
        all()
    if user:
        for data in user:
            db.session.delete(data)

    db.session.commit()
    return redirect('/admin/user')


@app.route('/admin/user/delete-all')
def delete_all_users():
    query = "truncate table artifact_show_windows cascade;"\
            "alter sequence artifact_show_windows_id_seq restart 1;"\
            "truncate table artifacts cascade;"\
            "alter sequence artifacts_id_seq restart 1;"\
            "truncate table dungeon_activities cascade;"\
            "alter sequence dungeon_activities_id_seq restart 1;"\
            "truncate table equipment_options cascade;"\
            "alter sequence equipment_options_id_seq restart 1;"\
            "truncate table equipments cascade;"\
            "alter sequence equipments_id_seq restart 1;"\
            "truncate table heroes cascade;"\
            "alter sequence heroes_id_seq restart 1;"\
            "truncate table users cascade;"\
            "alter sequence users_id_seq restart 1;"\
            "truncate table adventures cascade;"\
            "alter sequence adventures_id_seq restart 1;"\
            "truncate table league_duel_histories cascade;"\
            "alter sequence league_duel_histories_id_seq restart 1;"\
            "truncate table league_user_properties cascade;"\
            "alter sequence league_user_properties_id_seq restart 1;"\
            "truncate table mailboxes cascade;"\
            "alter sequence mailboxes_id_seq restart 1;"\
            "truncate table user_achievements cascade;"\
            "alter sequence user_achievements_id_seq restart 1;"\
            "truncate table achievements cascade;"\
            "alter sequence achievements_id_seq restart 1;"\
            "truncate table purchase_verification cascade;"\
            "alter sequence purchase_verification_id_seq restart 1;"\
            "truncate table user_short_term_properties cascade;"\
            "alter sequence user_short_term_properties_id_seq restart 1;"\
            "truncate table cash_shop_histories cascade;"\
            "alter sequence cash_shop_histories_id_seq restart 1;"

    db.session.execute(query)
    db.session.commit()
    return redirect('/admin/user')

