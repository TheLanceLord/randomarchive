import os
import json

with open('/home/damianlance/randomarchive/randomarchive/etc/config.json') as config_file:
    config = json.load(config_file)

class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    MYSQL_USER = config.get('MYSQL_USER')
    MYSQL_PASSWORD = config.get('MYSQL_PASSWORD')
    MYSQL_HOST = config.get('MYSQL_HOST')
    MYSQL_DB = config.get('MYSQL_DB')
    MYSQL_CURSORCLASS = config.get('MYSQL_CURSORCLASS')
    GCS_BUCKET_NAME = config.get('GCS_BUCKET_NAME')
    GCS_SERVICE_ACCOUNT_KEY = config.get('GCS_SERVICE_ACCOUNT_KEY')
    ORGANIZATION_ID = config.get('ORGANIZATION_ID')