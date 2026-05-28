# 📚 Wisme — 読書メモ × AI単語検索アプリ

本を読んで「この言葉、何だっけ？」ってなること、ありませんか？
ブラウザで調べるとタブが乱立、しかもなかなか覚えられない...  
**Wisme** は、読書メモと単語調べが１アプリにまとまった学習用アプリです。

---

## こんなことができます

- **①読書メモの管理** — 本や資料のタイトル・感想・章ごとのメモをまとめて記録
- **②AI単語検索** — 気になった単語を入力するだけで、Gemini AIが日本語で意味を解説
- **③単語帳機能とフラッシュカード機能** _ 習得した知識のアウトプット
- **④書籍サムネイル取得** — Google Books APIと連携してカバー画像を自動取得
- **⑤メール認証 / Google OAuth** — 安全なアカウント管理


---
## 機能選定の理由
私の趣味が読書ということもあり、読書メモアプリ作りを始めました。
特に文学や技術書を読んでいる際、知らない単語に出会うと思います。
その際、調べてタブが乱立したり、調べたタブを消すかどうか迷ったり、
消したら消したですぐ忘れてもう一度調べる羽目になったりした経験があり、
この面倒を解決しようと思ったため読書メモに単語検索機能を統合しようと考えました。
知識のアウトプットのため、単語を一覧で見られる単語帳機能と、
１つ１つ裏返して意味を隠せるフラッシュカード機能を追加しました。
途中メール認証で進めていたのですが、Googleアカウントでのログインが便利だったので、
Google OAuthを追加しました。



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
## 生成AIの利用

- **仕様モデル**：Gemini,Claude,claude code
- **なぜ使ったか**
  開発当初は学習のため、AIを使わずに作成していました。AIを使うとどうしても頼ってしまい
  分かったつもりになってしまうからです。主要機能（読書メモ機能、単語検索機能）の設計、実装を自力で行ったあと、
  Geminiやclaude codeを用いて、UI/UX、セキュリティ、単語帳・単語カード機能を追加しました。
  (これらのコミット履歴はwisme-deveopmentリポジトリにあります。)

- **使用時に気を付けていること**
  生成AIが出力したコードに疑問点があれば、解決するまで質問したり公式ドキュメントを参照したりしてから
  コードを採用しました。これまでの経験から、AIの出力は必ずしも正しいわけではなく、エラーを繰り返し吐いたり
  ただ動いているという状態になることもあることを学びました。コードレビューの精度を上げるべく、以下のようなプロンプトを用いて
  学んでいます。
  
- **コードリーディング時に使っているプロンプト例**
  あなたはプログラミング講師です。
  私の質問に対し、以下の要件を守ってください。
  ①答えを示すのではなく、答えに至るまでの考え方やヒントを出すこと。
  ②コード例を示す場合、30％程度の完成度で示すこと。
  ③設定ファイルの修正や環境構築に関してなど、「知らないとどうしようもないこと」
  はすぐに答えを示すこと。
  ④ただし「答えを教えてください」と私が明示した場合、答えを示すこと。


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

