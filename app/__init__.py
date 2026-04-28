import os
from flask import Flask
from .models.base import db
from .routes import main_bp, auth_bp, books_bp, profile_bp

def create_app(test_config=None):
    # 建立並設定 Flask 應用程式 (App Factory Pattern)
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(app.instance_path, 'database.db')),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_CONTENT_LENGTH=5 * 1024 * 1024 # 限制上傳檔案大小為 5MB
    )

    if test_config is None:
        # 當不是在測試環境時，嘗試讀取 instance/config.py 的設定
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 載入測試設定
        app.config.from_mapping(test_config)

    # 確保 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化第三方擴充套件 (例如 SQLAlchemy)
    db.init_app(app)

    # 註冊所有 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(profile_bp)

    return app
