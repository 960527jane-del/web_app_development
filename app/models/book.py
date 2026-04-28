from datetime import datetime
from .base import db

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    course_name = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='book', lazy=True, cascade="all, delete-orphan")
    favorites = db.relationship('Favorite', backref='book', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, **kwargs):
        """
        新增一筆 Book 記錄。
        參數: kwargs (包含 title, price, seller_id 等欄位)
        回傳: 成功時回傳 Book 實例，失敗時拋出例外。
        """
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            print(f"Error creating Book: {e}")
            raise

    @classmethod
    def get_by_id(cls, book_id):
        """
        透過 ID 取得單筆 Book 記錄。
        參數: book_id (int)
        回傳: Book 實例 或 None
        """
        try:
            return cls.query.get(book_id)
        except Exception as e:
            print(f"Error getting Book by ID: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有 Book 記錄。
        回傳: Book 實例列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all Books: {e}")
            return []
            
    @classmethod
    def search(cls, keyword):
        """
        透過書名進行模糊搜尋。
        參數: keyword (str)
        回傳: 匹配的 Book 實例列表
        """
        try:
            return cls.query.filter(cls.title.ilike(f'%{keyword}%')).all()
        except Exception as e:
            print(f"Error searching Books: {e}")
            return []

    def update(self, **kwargs):
        """
        更新 Book 記錄。
        參數: kwargs (包含要更新的欄位與值)
        回傳: 無
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating Book: {e}")
            raise

    def delete(self):
        """
        刪除 Book 記錄。
        回傳: 無
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Book: {e}")
            raise
