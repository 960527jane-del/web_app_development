from flask import Blueprint

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/', methods=['GET'])
def list_books():
    """
    輸入: (Optional) query string `q` 作為關鍵字搜尋
    處理邏輯: 若有 `q` 則對書名進行模糊搜尋，否則列出所有 available 狀態的書籍
    輸出: 渲染 book/list.html
    """
    pass

@books_bp.route('/new', methods=['GET', 'POST'])
def create_book():
    """
    輸入: GET無；POST包含 title, author, course_name, condition, price, image 圖片檔
    處理邏輯:
      - 需要 @login_required
      - GET: 顯示新增書籍表單
      - POST: 處理圖片上傳，儲存新 Book 實例
    輸出: 成功後導向該書籍詳情頁
    """
    pass

@books_bp.route('/<int:id>', methods=['GET'])
def book_detail(id):
    """
    輸入: 書籍 ID
    處理邏輯: 查詢該書籍，並載入關聯的 Messages (留言) 與賣家資訊
    輸出: 渲染 book/detail.html
    錯誤處理: 若找不到書籍則回傳 404
    """
    pass

@books_bp.route('/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    輸入: 書籍 ID
    處理邏輯:
      - 需要 @login_required 且目前使用者必須是該書的賣家 (seller_id)
      - 取得目前書籍資料供表單預填
    輸出: 渲染 book/edit.html (或共用的表單頁面)
    """
    pass

@books_bp.route('/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    輸入: 書籍 ID 與更新表單資料
    處理邏輯:
      - 需要 @login_required 且權限為賣家本人
      - 更新該筆書籍資料
    輸出: 導向書籍詳情頁
    """
    pass

@books_bp.route('/<int:id>/status', methods=['POST'])
def update_book_status(id):
    """
    輸入: 書籍 ID 與表單傳來的新狀態 (available, reserved, sold)
    處理邏輯:
      - 需要 @login_required 且權限為賣家本人
      - 更改資料庫 status 欄位
    輸出: 導向書籍詳情頁或個人頁面
    """
    pass

@books_bp.route('/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    輸入: 書籍 ID
    處理邏輯:
      - 需要 @login_required 且權限為賣家本人
      - 將書籍資料從資料庫刪除 (或標記為已下架)
    輸出: 導向個人頁面 (我的書櫃)
    """
    pass

@books_bp.route('/<int:id>/messages', methods=['POST'])
def add_message(id):
    """
    輸入: 書籍 ID 與留言內容 content
    處理邏輯:
      - 需要 @login_required
      - 建立 Message 紀錄，關聯此書與留言者
    輸出: 導向書籍詳情頁，顯示剛新增的留言
    """
    pass

@books_bp.route('/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """
    輸入: 書籍 ID
    處理邏輯:
      - 需要 @login_required
      - 檢查目前使用者是否已收藏此書，若有則刪除收藏，若無則新增收藏
    輸出: 重導向回書籍詳情頁
    """
    pass
