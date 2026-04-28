from datetime import datetime
from .base import db

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, **kwargs):
        """
        新增一筆 Favorite 記錄。
        參數: kwargs (包含 user_id, book_id)
        回傳: 成功時回傳 Favorite 實例，失敗時拋出例外。
        """
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            print(f"Error creating Favorite: {e}")
            raise

    @classmethod
    def get_by_id(cls, favorite_id):
        """
        透過 ID 取得單筆 Favorite 記錄。
        參數: favorite_id (int)
        回傳: Favorite 實例 或 None
        """
        try:
            return cls.query.get(favorite_id)
        except Exception as e:
            print(f"Error getting Favorite by ID: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有 Favorite 記錄。
        回傳: Favorite 實例列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all Favorites: {e}")
            return []

    @classmethod
    def get_by_user_id(cls, user_id):
        """
        透過使用者 ID 取得該使用者的所有收藏。
        參數: user_id (int)
        回傳: Favorite 實例列表
        """
        try:
            return cls.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error getting Favorites by user_id: {e}")
            return []

    def update(self, **kwargs):
        """
        更新 Favorite 記錄。
        參數: kwargs (包含要更新的欄位與值)
        回傳: 無
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating Favorite: {e}")
            raise

    def delete(self):
        """
        刪除 Favorite 記錄。
        回傳: 無
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Favorite: {e}")
            raise
