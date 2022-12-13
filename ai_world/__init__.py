from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, face_analysis_views # , question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(face_analysis_views.bp)
    app.config.update(
        # Flask-Dropzone config:
        DROPZONE_ALLOWED_FILE_TYPE='image',
        DROPZONE_MAX_FILE_SIZE=3,
        DROPZONE_MAX_FILES=20,
        DROPZONE_UPLOAD_ON_CLICK=True
    )
    dropzone = Dropzone(app)
    # app.register_blueprint(answer_views.bp)

    return app
