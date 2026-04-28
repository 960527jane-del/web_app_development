from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    輸入: 無
    處理邏輯: 查詢最新上架的書籍 (例如取最新 10 筆狀態為 available 的資料)
    輸出: 渲染 index.html
    錯誤處理: 無
    """
    pass
