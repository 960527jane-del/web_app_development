import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app.models.book import Book
from app.models.message import Message
from app.models.favorite import Favorite
from app.routes.auth import login_required

books_bp = Blueprint('books', __name__, url_prefix='/books')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@books_bp.route('/', methods=['GET'])
def list_books():
    """顯示所有書籍或搜尋結果"""
    query = request.args.get('q')
    if query:
        books = Book.search(query)
    else:
        books = Book.query.filter_by(status='available').order_by(Book.created_at.desc()).all()
    return render_template('book/list.html', books=books, query=query)

@books_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_book():
    """新增二手書"""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        course_name = request.form.get('course_name')
        condition = request.form.get('condition')
        price = request.form.get('price')
        image = request.files.get('image')
        
        if not title or not condition or not price:
            flash('書名、書況與價格為必填欄位', 'danger')
            return render_template('book/edit.html')
            
        try:
            price = int(price)
        except ValueError:
            flash('價格必須是數字', 'danger')
            return render_template('book/edit.html')

        image_path = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'images')
            os.makedirs(upload_folder, exist_ok=True)
            path = os.path.join(upload_folder, filename)
            image.save(path)
            image_path = f'images/{filename}'
            
        try:
            book = Book.create(
                seller_id=session['user_id'],
                title=title,
                author=author,
                course_name=course_name,
                condition=condition,
                price=price,
                image_path=image_path
            )
            flash('上架成功！', 'success')
            return redirect(url_for('books.book_detail', id=book.id))
        except Exception as e:
            flash('上架失敗，請稍後再試', 'danger')

    return render_template('book/edit.html', book=None)

@books_bp.route('/<int:id>', methods=['GET'])
def book_detail(id):
    """顯示單一書籍詳細資訊與留言"""
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍', 'danger')
        return redirect(url_for('books.list_books'))
        
    messages = Message.get_by_book_id(id)
    
    is_favorite = False
    if session.get('user_id'):
        fav = Favorite.query.filter_by(user_id=session['user_id'], book_id=id).first()
        if fav:
            is_favorite = True
            
    return render_template('book/detail.html', book=book, messages=messages, is_favorite=is_favorite)

@books_bp.route('/<int:id>/edit', methods=['GET'])
@login_required
def edit_book(id):
    """顯示編輯表單"""
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍', 'danger')
        return redirect(url_for('books.list_books'))
        
    if book.seller_id != session['user_id']:
        flash('您沒有權限編輯此書籍', 'danger')
        return redirect(url_for('books.book_detail', id=id))
        
    return render_template('book/edit.html', book=book)

@books_bp.route('/<int:id>/update', methods=['POST'])
@login_required
def update_book(id):
    """更新書籍資料"""
    book = Book.get_by_id(id)
    if not book or book.seller_id != session['user_id']:
        flash('找不到該書籍或無權限', 'danger')
        return redirect(url_for('books.list_books'))
        
    title = request.form.get('title')
    author = request.form.get('author')
    course_name = request.form.get('course_name')
    condition = request.form.get('condition')
    price = request.form.get('price')
    
    if not title or not condition or not price:
        flash('書名、書況與價格為必填', 'danger')
        return redirect(url_for('books.edit_book', id=id))
        
    try:
        book.update(
            title=title,
            author=author,
            course_name=course_name,
            condition=condition,
            price=int(price)
        )
        flash('書籍資訊更新成功', 'success')
    except Exception as e:
        flash('更新失敗', 'danger')
        
    return redirect(url_for('books.book_detail', id=id))

@books_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_book_status(id):
    """更新交易狀態"""
    book = Book.get_by_id(id)
    if not book or book.seller_id != session['user_id']:
        flash('無權限操作', 'danger')
        return redirect(url_for('books.list_books'))
        
    status = request.form.get('status')
    if status in ['available', 'reserved', 'sold']:
        try:
            book.update(status=status)
            flash('交易狀態已更新', 'success')
        except Exception:
            flash('狀態更新失敗', 'danger')
            
    return redirect(url_for('books.book_detail', id=id))

@books_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_book(id):
    """刪除書籍"""
    book = Book.get_by_id(id)
    if not book or book.seller_id != session['user_id']:
        flash('無權限操作', 'danger')
        return redirect(url_for('books.list_books'))
        
    try:
        book.delete()
        flash('書籍已成功刪除', 'success')
    except Exception:
        flash('刪除失敗', 'danger')
        
    return redirect(url_for('profile.index'))

@books_bp.route('/<int:id>/messages', methods=['POST'])
@login_required
def add_message(id):
    """新增留言"""
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍', 'danger')
        return redirect(url_for('books.list_books'))
        
    content = request.form.get('content')
    if not content:
        flash('留言內容不可為空', 'warning')
    else:
        try:
            Message.create(
                book_id=id,
                sender_id=session['user_id'],
                content=content
            )
            flash('留言成功', 'success')
        except Exception:
            flash('留言失敗', 'danger')
            
    return redirect(url_for('books.book_detail', id=id))

@books_bp.route('/<int:id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(id):
    """加入/取消收藏"""
    fav = Favorite.query.filter_by(user_id=session['user_id'], book_id=id).first()
    try:
        if fav:
            fav.delete()
            flash('已取消收藏', 'info')
        else:
            Favorite.create(user_id=session['user_id'], book_id=id)
            flash('已成功加入收藏！', 'success')
    except Exception:
        flash('操作失敗', 'danger')
        
    return redirect(url_for('books.book_detail', id=id))
