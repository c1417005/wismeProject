# 📚 Wisme — 読書メモ × AI単語検索アプリ

本を読んで「この言葉、何だっけ？」ってなること、ありませんか？
ブラウザで調べるとタブが乱立、しかもなかなか覚えられない...  
**Wisme** は、読書メモを残しながら気になった単語の意味をAIにサクッと調べてもらえるWebアプリです！

---

## こんなことができます

- **読書メモの管理** — 本や資料のタイトル・感想・章ごとのメモをまとめて記録
- **AI単語検索** — 気になった単語を入力するだけで、Gemini AIが日本語で意味を解説
- **書籍サムネイル取得** — Google Books APIと連携してカバー画像を自動取得
- **単語とメモの紐付け** — 調べた単語は次に保存したメモに自動でリンク
- **メール認証 / Google OAuth** — 安全なアカウント管理

---

## Try it!
https://wisme-6f0eee63bb26.herokuapp.com/
デモユーザーのログイン情報
メールアドレス:demo@example.com
パスワード:demo123
## 技術スタック

| カテゴリ | 使用技術 |
|---|---|
| バックエンド | Django 6.0.2 / Python 3.13 |
| 認証 | django-allauth（メール認証 + Google OAuth） |
| AI | Google Gemini 2.5 Flash |
| 書籍情報 | Google Books API |
| ストレージ | Cloudinary（メディア）/ WhiteNoise（静的ファイル） |
| DB | SQLite（開発）/ PostgreSQL（本番） |
| デプロイ | Gunicorn + Procfile |
| i18n | 日本語・英語対応 |

---

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、各値を設定してください。

```bash
cp .env.example .env
```

```
DEBUG=True
SECRET_KEY=なんでもOK
GOOGLE_GEMINI_API_KEY=必須（単語検索に使います）
GOOGLE_BOOKS_API_KEY=任意（書籍サムネイル取得に使います）
FIELD_ENCRYPTION_KEY=Fernetキー（下記コマンドで生成）
CLOUD_NAME=Cloudinaryの認証情報
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

`FIELD_ENCRYPTION_KEY` の生成：

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### 3. DBのセットアップ & 起動

```bash
python manage.py migrate
python manage.py runserver
```

ブラウザで `http://localhost:8000` を開けば完成です！

---

## よく使うコマンド

```bash
# テスト実行
python manage.py test

# 翻訳ファイルのコンパイル
python manage.py compilemessages

# 静的ファイルの収集（本番用）
python manage.py collectstatic
```

---

