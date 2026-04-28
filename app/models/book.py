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
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def get_by_id(cls, book_id):
        return cls.query.get(book_id)

    @classmethod
    def get_all(cls):
        return cls.query.all()
        
    @classmethod
    def search(cls, keyword):
        return cls.query.filter(cls.title.ilike(f'%{keyword}%')).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
