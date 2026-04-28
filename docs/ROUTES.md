# 路由設計文件

本文件依據 PRD、系統架構與資料庫設計，規劃了二手書平台的 URL 路由結構、HTTP 方法以及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能區塊 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `index.html` | 顯示首頁商品列表預覽 |
| **會員** | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單頁面 |
| **會員** | POST | `/auth/register` | — | 接收註冊表單，寫入資料庫後導向登入頁 |
| **會員** | GET | `/auth/login` | `auth/login.html` | 顯示登入表單頁面 |
| **會員** | POST | `/auth/login` | — | 驗證帳密，建立 Session 後導向首頁 |
| **會員** | GET | `/auth/logout` | — | 清除 Session 狀態，導向首頁 |
| **書籍** | GET | `/books` | `book/list.html` | 顯示所有書籍列表與關鍵字搜尋結果 |
| **書籍** | GET | `/books/new` | `book/edit.html` | 顯示新增二手書表單 (需登入) |
| **書籍** | POST | `/books/new` | — | 接收表單並儲存書籍資訊，導向書籍詳情頁 |
| **書籍** | GET | `/books/<id>` | `book/detail.html` | 顯示單一書籍詳細資訊與下方留言區 |
| **書籍** | GET | `/books/<id>/edit` | `book/edit.html` | 顯示編輯現有書籍表單 (限賣家) |
| **書籍** | POST | `/books/<id>/update` | — | 更新書籍資料，導向書籍詳情頁 |
| **書籍** | POST | `/books/<id>/status` | — | 切換交易狀態(上架中/保留/已售出) |
| **書籍** | POST | `/books/<id>/delete` | — | 刪除該書籍，導向個人書櫃 |
| **互動** | POST | `/books/<id>/messages` | — | 接收留言內容並儲存，導向書籍詳情頁 |
| **互動** | POST | `/books/<id>/favorite` | — | 加入/取消收藏，導向書籍詳情頁 |
| **個人** | GET | `/profile` | `profile/index.html` | 顯示個人資料與我的上架書籍 |
| **個人** | GET | `/profile/favorites`| `profile/favorites.html`| 顯示我的收藏清單 |

## 2. 每個路由的詳細說明

### 首頁 (Main)
- **`GET /`**
  - 輸入：無
  - 邏輯：從 `Book` Model 撈取最新上架（且狀態為 available）的書籍清單。
  - 輸出：渲染 `index.html`

### 會員 (Auth)
- **`GET /auth/register`** 與 **`POST /auth/register`**
  - 輸入：表單欄位（email, name, password）。
  - 邏輯：檢查 email 是否重複，將密碼雜湊加密後存入 `User`。
  - 錯誤處理：若 email 重複，透過 `flash` 顯示錯誤訊息並重新渲染註冊頁。
- **`GET /auth/login`** 與 **`POST /auth/login`**
  - 輸入：表單欄位（email, password）。
  - 邏輯：比對 email 與密碼，成功則將 user_id 寫入 session。

### 書籍 (Books)
- **`GET /books`**
  - 輸入：URL 參數 `?q=關鍵字`。
  - 邏輯：若有 `q` 則搜尋 `title`，否則列出所有書籍。
- **`POST /books/new`**
  - 邏輯：驗證 `@login_required`。處理圖片上傳至 static/images，建立 `Book` 實例。
- **`GET /books/<id>`**
  - 邏輯：透過 `id` 查詢 `Book`。若查無此書回傳 404。同時載入關聯的 `Message` 與 `User`。
- **`POST /books/<id>/update`** 與 **`POST /books/<id>/delete`**
  - 邏輯：必須驗證 `@login_required` 且目前登入者必須與該書籍的 `seller_id` 相同，避免越權操作。

### 互動 (Messages & Favorites)
- **`POST /books/<id>/messages`**
  - 邏輯：驗證 `@login_required`。建立 `Message` 實例。
- **`POST /books/<id>/favorite`**
  - 邏輯：檢查是否已收藏，若有則刪除 `Favorite`，若無則新增，實現 toggle 功能。

### 個人頁面 (Profile)
- **`GET /profile`**
  - 邏輯：驗證 `@login_required`。撈取目前登入者的基本資料與關聯的書籍清單。

## 3. Jinja2 模板清單

所有模板皆繼承自 `base.html`，以保持共同的導覽列與頁尾：

- `base.html` (共同外觀、Header、Footer、Flash 訊息顯示)
- `index.html` (首頁)
- `auth/login.html` (登入頁)
- `auth/register.html` (註冊頁)
- `book/list.html` (搜尋結果/書籍列表)
- `book/detail.html` (單一商品詳情，包含留言板)
- `book/edit.html` (新增/編輯共用的表單頁)
- `profile/index.html` (個人書櫃)
- `profile/favorites.html` (我的收藏)

## 4. 路由骨架程式碼

相關的 Python 函式骨架已在 `app/routes/` 資料夾下建立。
