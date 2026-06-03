# 02. Page/Chapter API実装

## 背景・目的

読書メモ（Page）とその章（Chapter）に対するCRUD APIをDRFで実装する。これがWismeの中核機能であり、React化の最初の対象。

既存ロジックの再現が必要なポイント:
- Pageは `UUID` 主キー
- `Chapter` は `Page` に対する nested リソース（`related_name='chapters'`）。`order` で並び順管理
- `PageForm` + `ChapterFormSet` の保存時に `order = idx` が再採番される
- Page保存時、`SearchedWord.objects.filter(note__isnull=True)` を新Pageに自動関連付け
- `picture`（Cloudinaryアップロード）と `image_url`（Google Books由来）の二系統

## 提案するエンドポイント

```
GET    /api/v1/pages/                  ページ一覧（自分のみ、降順、ページネーション）
POST   /api/v1/pages/                  作成（multipart 対応、chapters ネスト書き込み）
GET    /api/v1/pages/{uuid}/           詳細（chapters, words を埋め込み）
PATCH  /api/v1/pages/{uuid}/           部分更新
PUT    /api/v1/pages/{uuid}/           全更新
DELETE /api/v1/pages/{uuid}/           削除
```

## 受け入れ基準（DoD）

- [ ] `wisme/api/serializers.py` に `PageSerializer`, `ChapterSerializer`, `PageDetailSerializer`（words含む）
- [ ] `wisme/api/views.py` に `PageViewSet`（ModelViewSet）を実装
  - 自分のページのみ返す（`get_queryset` を owner でフィルタ）
  - `perform_create` で `owner=request.user` を設定
  - `perform_create` 後に `SearchedWord.objects.filter(note__isnull=True, owner=request.user).update(note=instance)` を実行（既存ロジック移植）
- [ ] `chapters` を nested writable に対応（`drf-writable-nested` 採用 or 手動実装）
- [ ] `picture` の multipart アップロードに対応（Cloudinary経由で保存）
- [ ] 他人のページに対する取得・編集・削除が403になることをテスト
- [ ] テスト: `wisme/tests/test_page_api.py`
  - 一覧（自分のみ表示）
  - 作成（chapters あり/なし）
  - 作成時の未関連 SearchedWord 自動紐付け
  - 更新（chapter追加・削除・並び替え）
  - 削除
  - 権限（403/404）
- [ ] OpenAPIスキーマ確認用に `drf-spectacular` の導入を検討（任意）

## 作業手順

1. Serializer 作成（Chapter → Page 順、Page側で chapters ネスト）
2. ViewSet 作成 + ルーティング（`DefaultRouter` で登録）
3. multipart 対応のためのパーサー設定（`MultiPartParser, FormParser` 追加）
4. Chapter保存時の `order` 再採番ロジック移植
5. SearchedWord自動紐付けロジック移植
6. テスト作成・実行
7. テンプレート版（`PageCreateView` 等）は **削除せず残す**

## 依存・優先度

- **依存**: #01
- **ブロックする**: #06, #07, #08
- **優先度**: 高
- **想定工数**: 1日

## 注意点

- `Chapter.order` を hidden field として React 側で並び順管理する想定。サーバー側でも再採番してロバストにする
- `picture` 更新時、旧画像の削除はCloudinaryStorageの挙動を確認（モデル側で `delete` をオーバーライド済みなので一旦そのまま）
