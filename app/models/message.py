from datetime import datetime
from .base import db

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, **kwargs):
        """
        新增一筆 Message 記錄。
        參數: kwargs (包含 book_id, sender_id, content)
        回傳: 成功時回傳 Message 實例，失敗時拋出例外。
        """
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            print(f"Error creating Message: {e}")
            raise

    @classmethod
    def get_by_id(cls, message_id):
        """
        透過 ID 取得單筆 Message 記錄。
        參數: message_id (int)
        回傳: Message 實例 或 None
        """
        try:
            return cls.query.get(message_id)
        except Exception as e:
            print(f"Error getting Message by ID: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有 Message 記錄。
        回傳: Message 實例列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all Messages: {e}")
            return []

    @classmethod
    def get_by_book_id(cls, book_id):
        """
        透過書籍 ID 取得該書所有的留言，並按時間排序。
        參數: book_id (int)
        回傳: Message 實例列表
        """
        try:
            return cls.query.filter_by(book_id=book_id).order_by(cls.created_at.asc()).all()
        except Exception as e:
            print(f"Error getting Messages by book_id: {e}")
            return []

    def update(self, **kwargs):
        """
        更新 Message 記錄。
        參數: kwargs (包含要更新的欄位與值)
        回傳: 無
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating Message: {e}")
            raise

    def delete(self):
        """
        刪除 Message 記錄。
        回傳: 無
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Message: {e}")
            raise
