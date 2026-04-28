# 流程圖文件

本文件依據 PRD 與系統架構文件，視覺化使用者操作路徑與系統資料流，幫助開發團隊釐清網站互動與資料處理流程。

## 1. 使用者流程圖（User Flow）

呈現使用者從進入首頁後，各種主要功能的操作路徑。

```mermaid
flowchart LR
    A([進入網站首頁]) --> B{是否已登入？}
    
    B -->|否| C[瀏覽書籍列表/搜尋]
    C --> D[點擊書籍查看詳情]
    D --> E{想購買或留言？}
    E -->|是| F[引導至登入/註冊頁面]
    F --> G[註冊新帳號或登入]
    G --> B
    
    B -->|是| H[登入狀態操作]
    H --> I[瀏覽書籍與搜尋]
    I --> J[書籍詳情頁]
    J --> K[發送留言/聯絡賣家]
    J --> Q[加入收藏]
    
    H --> L[個人書櫃與帳號管理]
    L --> M[新增上架二手書]
    L --> N[編輯現有書籍資訊]
    L --> O[切換書籍狀態/下架]
    L --> P[查看我的收藏清單]
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖描述「使用者上架一本二手書」時，從前端表單送出到資料存入資料庫的完整互動流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask Route (Controller)
    participant Model as Book Model
    participant DB as SQLite 資料庫

    User->>Browser: 填寫書籍資訊(名稱、照片、價格等)並送出
    Browser->>Flask: POST /books/new (帶上表單資料與圖片檔案)
    Flask->>Flask: 驗證是否登入 (@login_required)
    Flask->>Flask: 處理圖片上傳並儲存至 static/images
    Flask->>Model: 建立新的 Book 實例 (包含圖片路徑)
    Model->>DB: INSERT INTO books (...)
    DB-->>Model: 回傳成功並賦予新 ID
    Model-->>Flask: 儲存成功
    Flask-->>Browser: HTTP 302 重導向 (Redirect) 至該書籍詳情頁
    Browser->>User: 顯示上架成功的書籍畫面
```

## 3. 功能清單對照表

將 PRD 中的功能需求對應至網站的 URL 路徑與 HTTP 方法，作為後續開發路由（Routes）的依據。

| 功能區塊 | 功能說明 | HTTP 方法 | URL 路徑 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與探索** | 首頁 / 最新書籍列表 | GET | `/` | 預設顯示最新上架的書籍 |
| | 書籍搜尋與列表 | GET | `/books` | 可透過 `?q=關鍵字` 參數進行搜尋 |
| | 書籍詳情頁 | GET | `/books/<int:id>` | 顯示單一書籍的詳細資訊與留言 |
| **會員認證** | 註冊帳號 | GET / POST | `/auth/register` | 填寫學生資訊並建立帳號 |
| | 登入系統 | GET / POST | `/auth/login` | 驗證密碼並建立 session |
| | 登出系統 | GET | `/auth/logout` | 清除 session |
| **書櫃管理** | 個人頁面與我的書籍 | GET | `/profile` | 顯示自己上架的書籍與基本資料 |
| | 新增二手書 | GET / POST | `/books/new` | 顯示表單 / 接收資料並存檔 |
| | 編輯書籍資訊 | GET / POST | `/books/<int:id>/edit` | 修改現有書籍內容 |
| | 下架 / 刪除書籍 | POST | `/books/<int:id>/delete` | 將書籍下架或刪除 |
| | 狀態切換 | POST | `/books/<int:id>/status` | 變更書籍交易狀態(上架/保留/售出) |
| **互動功能** | 新增留言 | POST | `/books/<int:id>/messages` | 在書籍下方留言詢問 |
| | 我的收藏 (加分項) | GET | `/profile/favorites` | 查看已收藏的書籍清單 |
| | 加入/取消收藏 (加分項)| POST | `/books/<int:id>/favorite` | 將書籍加入或移出收藏 |
