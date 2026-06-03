# 04. BookThumbnail/Feedback/Profile/Dashboard API実装

## 背景・目的

ページ・単語以外の補助的なAPIをまとめて実装する。粒度が小さいため1チケットに集約。

対象:
- 書籍サムネ検索（Google Books）
- フィードバック送信
- ユーザープロフィール取得/更新（display_name, profile_image）
- ダッシュボード用集計（ページ数、最終更新ページ）

## 提案するエンドポイント

```
GET   /api/v1/books/thumbnails/?title=&author=    書籍サムネ候補リスト
GET   /api/v1/me/                                 自分のプロフィール取得
PATCH /api/v1/me/                                 プロフィール更新（multipart対応）
GET   /api/v1/dashboard/                          { page_count, latest_page, last_updated_at }
POST  /api/v1/feedback/                           フィードバック送信
```

## 受け入れ基準（DoD）

- [ ] 各エンドポイントを実装し `wisme/api/urls.py` に登録
- [ ] `UserProfileSerializer`（display_name, profile_image, email等）
- [ ] `FeedbackSerializer`（message のみ受け取り、owner はサーバー側で付与）
- [ ] `DashboardSerializer` または APIView で集計値を返す
- [ ] 書籍サムネ検索は既存 `BookThumbnailService.search` を流用
- [ ] テスト: 各エンドポイントの正常系1ケース + 認可ケース
- [ ] 旧テンプレートエンドポイント（`/wisme/books/thumbnail/` 等）は維持

## 作業手順

1. Serializer群を作成
2. 各View/ViewSet 実装
3. ルーティング登録
4. テスト

## 依存・優先度

- **依存**: #01
- **ブロックする**: #08（書籍サムネ）, #11（プロフィール）, #12（ダッシュボード/フィードバック）
- **優先度**: 中
- **想定工数**: 0.5日
