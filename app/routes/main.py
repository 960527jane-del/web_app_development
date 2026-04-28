from flask import Blueprint, render_template
from app.models.book import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    輸入: 無
    處理邏輯: 查詢最新上架的書籍 (取最新 10 筆狀態為 available 的資料)
    輸出: 渲染 index.html
    錯誤處理: 無
    """
    books = Book.query.filter_by(status='available').order_by(Book.created_at.desc()).limit(10).all()
    return render_template('index.html', books=books)
