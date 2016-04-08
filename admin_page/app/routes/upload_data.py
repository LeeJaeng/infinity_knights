from flask import render_template, request

from app import DATA_VERSION
from app import app, bucket
from app.routes import insert_metadata

UPLOAD_DIR = "app/static/data/"
ALLOWED_EXTENTIONS = set(['csv'])

"""
    # ROUTE : upload_data.py
    # DESCRIPTION
        # /admin/upload-data에서 관리자가 Type과 파일을 입력한 뒤에 여기로 옴
        # 초기 app/__init__.py에서 설정한 bucket을 이용해서 AWS S3에 업로드 시킴
        # 그 파일을 일시적으로 UPLOAD_DIR에 저장을 한 뒤
        # db_insert() 실행하여 실제로 데이터베이스에 집어 넣는다.

"""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENTIONS


@app.route('/admin/upload-data', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'GET':
        return render_template('upload_data.html')

    elif request.method == 'POST':
        data_type = request.form.get('data_type')
        file = request.files['file']

    if file and allowed_file(file.filename):
        bucket_key = bucket.new_key(str(DATA_VERSION) + '/' + file.filename)
        # bucket에 저장한다
        bucket_key.set_contents_from_file(file)
        bucket_key.make_public()
        print(file.filename + ' s3 uploaded.')

        if file.filename.find(data_type) == 0:
            print(file.filename + ' db inserted.')
            # 이걸 async로
            insert_metadata.db_insert(data_type, bucket_key, file.filename)
        else:
            print('type mismatching')
        return render_template('upload_data.html', message="Success!", data_type=data_type, filename=file.filename)
    else:
        return render_template('upload_data.html', message="Failure!")
