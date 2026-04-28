from app import create_app
from app.models.base import db

app = create_app()

if __name__ == '__main__':
    # 在啟動時自動建立資料庫所有的表格
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
