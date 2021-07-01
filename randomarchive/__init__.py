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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from randomarchive.config import Config

db = SQLAlchemy()
mysql = MySQL()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mysql.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from randomarchive.users.routes import users
    from randomarchive.posts.routes import posts
    from randomarchive.main.routes import main
    from randomarchive.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
