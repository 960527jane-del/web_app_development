from flask import Blueprint

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
def index():
    """
    輸入: 無
    處理邏輯:
      - 需要 @login_required
      - 查詢目前登入使用者的資料，以及他所上架的所有書籍清單
    輸出: 渲染 profile/index.html
    """
    pass

@profile_bp.route('/favorites', methods=['GET'])
def favorites():
    """
    輸入: 無
    處理邏輯:
      - 需要 @login_required
      - 查詢目前登入使用者所收藏的所有書籍紀錄
    輸出: 渲染 profile/favorites.html
    """
    pass
