# 01. DRF基盤導入と認証/CORS設定

## 背景・目的

Djangoに `djangorestframework` を導入し、APIエンドポイント用の基盤（ルーティング、認証、権限、ページネーション、エラーハンドリング）を整える。後続のAPIチケット（02〜04）の前提となる。

既存のテンプレートview/URL（`/wisme/...`）は維持したまま、新規に `/api/v1/` 配下を切り出す。

## 受け入れ基準（DoD）

- [ ] `djangorestframework` を `requirements.txt` に追加
- [ ] `config/settings.py` に `REST_FRAMEWORK` 設定を追加
  - DefaultAuthenticationClasses: SessionAuthentication
  - DefaultPermissionClasses: IsAuthenticated
  - DefaultPaginationClass: PageNumberPagination（page_size=20）
- [ ] `config/urls.py` に `path('api/v1/', include('wisme.api.urls'))` を追加
- [ ] `wisme/api/` ディレクトリを作成（`__init__.py`, `urls.py`, `views.py`, `serializers.py`, `permissions.py`）
- [ ] 動作確認用に `/api/v1/health/` を作成し、ログイン済みユーザーに200を返す
- [ ] 未ログイン時は403を返すことを確認
- [ ] 既存のテンプレートview（`/wisme/page/list/` 等）は引き続き動作する
- [ ] 開発時のCORS設定（ViteのデフォルトポートからのアクセスをDEBUG時のみ許可）
  - `django-cors-headers` 導入、`CORS_ALLOWED_ORIGINS` を環境変数化
- [ ] CSRF設定の確認（同一オリジン運用なら `CSRF_TRUSTED_ORIGINS` 調整、別オリジン運用なら `CSRF_COOKIE_SAMESITE` 等を要検討）
- [ ] テスト（`wisme/tests/test_api_health.py`）を追加

## 作業手順

1. `pip install djangorestframework django-cors-headers` → `requirements.txt` 更新
2. `INSTALLED_APPS` に `'rest_framework'`, `'corsheaders'` 追加
3. `MIDDLEWARE` に `corsheaders.middleware.CorsMiddleware` を追加（CommonMiddlewareより前）
4. `REST_FRAMEWORK` / `CORS_ALLOWED_ORIGINS` 設定
5. `wisme/api/` ディレクトリと最低限のhealth endpointを実装
6. `config/urls.py` 更新
7. テスト追加・実行 → `python manage.py test`
8. `.env.example` に `CORS_ALLOWED_ORIGINS` を追記

## 依存・優先度

- **依存**: #00
- **ブロックする**: #02, #03, #04
- **優先度**: 高
- **想定工数**: 1日
