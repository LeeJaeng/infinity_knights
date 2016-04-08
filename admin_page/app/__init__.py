import os

from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['CONFIG_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')
app.config.from_pyfile(os.path.join(app.config.get('CONFIG_DIR'), 'secret.cfg'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]

app.debug = True

db = SQLAlchemy(app)

from app.models import *

# AWS S3 Connection
import boto
import boto.s3.connection

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

conn = boto.connect_s3(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    calling_format=boto.s3.connection.OrdinaryCallingFormat(),
)
bucket = conn.get_bucket(S3_BUCKET_NAME)
print("s3 connection.")

# metadata_version
DATA_VERSION = 1

from app.routes import *
