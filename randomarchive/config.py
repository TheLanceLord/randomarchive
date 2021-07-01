# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
import os
import json

with open('/randomarchive/randomarchive/etc/config.json') as config_file:
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
