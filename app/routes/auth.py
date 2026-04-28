from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    輸入: GET 無；POST 包含 email, password, name
    處理邏輯: 
      - GET: 顯示註冊表單
      - POST: 驗證 email 是否存在，建立 User 並將密碼加密存入資料庫
    輸出: 成功註冊後導向登入頁，失敗返回表單並顯示錯誤訊息
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    輸入: GET 無；POST 包含 email, password
    處理邏輯:
      - GET: 顯示登入表單
      - POST: 查詢 User 並驗證密碼，成功則建立 session (例如寫入 user_id)
    輸出: 成功登入後導向首頁，失敗返回表單並顯示錯誤
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    輸入: 無
    處理邏輯: 清除 session 中的 user_id 狀態
    輸出: 導向首頁
    """
    pass
