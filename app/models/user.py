from datetime import datetime
from .base import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    books = db.relationship('Book', backref='seller', lazy=True)
    messages = db.relationship('Message', backref='sender', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    @classmethod
    def create(cls, **kwargs):
        """
        新增一筆 User 記錄。
        參數: kwargs (包含 email, password_hash, name 等)
        回傳: 成功時回傳 User 實例，失敗時拋出例外。
        """
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            print(f"Error creating User: {e}")
            raise

    @classmethod
    def get_by_id(cls, user_id):
        """
        透過 ID 取得單筆記錄。
        參數: user_id (int)
        回傳: User 實例 或 None
        """
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error getting User by ID: {e}")
            return None

    @classmethod
    def get_by_email(cls, email):
        """
        透過 Email 取得單筆記錄。
        參數: email (str)
        回傳: User 實例 或 None
        """
        try:
            return cls.query.filter_by(email=email).first()
        except Exception as e:
            print(f"Error getting User by email: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有 User 記錄。
        回傳: User 實例列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all Users: {e}")
            return []

    def update(self, **kwargs):
        """
        更新 User 記錄。
        參數: kwargs (包含要更新的欄位與值)
        回傳: 無
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating User: {e}")
            raise

    def delete(self):
        """
        刪除 User 記錄。
        回傳: 無
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting User: {e}")
            raise
