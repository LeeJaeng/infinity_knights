from app import app
from flask import redirect
from app.routes.users import users, edit_user_properties
from app.routes.upload_data import upload_data


@app.route('/admin')
def index():
    return redirect('/admin/user')

