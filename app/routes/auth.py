from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
import functools

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    """自訂驗證登入的裝飾器"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            flash('請先登入後再進行操作', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    輸入: GET 無；POST 包含 email, password, name
    處理邏輯: 
      - GET: 顯示註冊表單
      - POST: 驗證 email 是否存在，建立 User 並將密碼加密存入資料庫
    輸出: 成功註冊後導向登入頁，失敗返回表單並顯示錯誤訊息
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if not email or not password or not name:
            flash('所有欄位皆為必填！', 'danger')
            return render_template('auth/register.html')
            
        existing_user = User.get_by_email(email)
        if existing_user:
            flash('此 Email 已被註冊！', 'danger')
            return render_template('auth/register.html')
            
        try:
            User.create(
                email=email,
                name=name,
                password_hash=generate_password_hash(password)
            )
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('註冊過程中發生錯誤，請稍後再試', 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    輸入: GET 無；POST 包含 email, password
    處理邏輯:
      - GET: 顯示登入表單
      - POST: 查詢 User 並驗證密碼，成功則建立 session (例如寫入 user_id)
    輸出: 成功登入後導向首頁，失敗返回表單並顯示錯誤
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('請輸入 Email 與密碼', 'warning')
            return render_template('auth/login.html')
            
        user = User.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash(f'登入成功！歡迎回來，{user.name}', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email 或密碼錯誤', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    輸入: 無
    處理邏輯: 清除 session 中的 user_id 狀態
    輸出: 導向首頁
    """
    session.clear()
    flash('您已成功登出', 'success')
    return redirect(url_for('main.index'))
