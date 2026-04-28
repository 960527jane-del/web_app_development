from flask import Blueprint, render_template, session
from app.models.user import User
from app.models.favorite import Favorite
from app.routes.auth import login_required

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
@login_required
def index():
    """
    輸入: 無
    處理邏輯: 查詢目前登入使用者的資料，以及他所上架的所有書籍清單
    輸出: 渲染 profile/index.html
    """
    user = User.get_by_id(session['user_id'])
    books = user.books
    return render_template('profile/index.html', user=user, books=books)

@profile_bp.route('/favorites', methods=['GET'])
@login_required
def favorites():
    """
    輸入: 無
    處理邏輯: 查詢目前登入使用者所收藏的所有書籍紀錄
    輸出: 渲染 profile/favorites.html
    """
    favs = Favorite.get_by_user_id(session['user_id'])
    # 從收藏紀錄中抓出實際的書籍物件
    books = [fav.book for fav in favs if fav.book]
    return render_template('profile/favorites.html', books=books)
