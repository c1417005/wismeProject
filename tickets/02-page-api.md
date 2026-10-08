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

- [x] `wisme/api/serializers.py` に `PageSerializer`, `ChapterSerializer`, `PageDetailSerializer`（words含む）
- [x] `wisme/api/views.py` に `PageViewSet`（ModelViewSet）を実装
  - 自分のページのみ返す（`get_queryset` を owner でフィルタ）
  - `perform_create` で `owner=request.user` を設定
  - `perform_create` 後に `SearchedWord.objects.filter(note__isnull=True, owner=request.user).update(note=instance)` を実行（既存ロジック移植）
- [x] `chapters` を nested writable に対応（`drf-writable-nested` 採用 or 手動実装）
- [x] `picture` の multipart アップロードに対応（Cloudinary経由で保存）
- [x] 他人のページに対する取得・編集・削除が404になることをテスト（owner で queryset を絞るため、存在を漏らさない 404 を採用）
- [x] テスト: `wisme/tests/test_page_api.py`
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

## 追加対応: 画像アップロードの分離

### 背景

現状は `POST/PATCH /api/v1/pages/` に multipart で `picture` と `chapters` を同時送信している。multipart はネスト配列を表現できないため `chapters` を JSON 文字列で送り、`PageSerializer.to_internal_value` で `json.loads` している。この変換がフロント・サーバー双方の複雑さの原因になっている。表紙画像は作成時に1回設定する程度で頻繁に変更されないため、ページ本体と画像の送信を分ける。

### 方針

ページ（+chapters）を JSON で先に保存し、返却された id に対して画像だけを multipart で送る。

```
POST   /api/v1/pages/                  作成（JSON のみ、chapters ネスト書き込み）
PATCH  /api/v1/pages/{uuid}/           部分更新（JSON のみ）
PUT    /api/v1/pages/{uuid}/picture/   表紙画像のアップロード／差し替え（multipart）
DELETE /api/v1/pages/{uuid}/picture/   表紙画像の削除
```

画像を先に送る方式は採らない。保存先の Page が存在しない段階で画像を保持する一時モデル・所有者チェック・放置画像の掃除が新たに必要になるため。

### 受け入れ基準（DoD）

- [x] `PageViewSet.parser_classes` を `JSONParser` のみにする
- [x] `PageViewSet` に `@action(detail=True, methods=['put', 'delete'], url_path='picture', parser_classes=[MultiPartParser])` を追加
  - 権限は既存の `get_object()` + `IsOwner` を利用（他人のページは404）
  - `PUT` は画像専用の Serializer（`picture` のみ）で検証・保存し、ページを返す
  - `DELETE` は `picture` を空にする
- [x] `PageSerializer` から `to_internal_value`（chapters の JSON 文字列変換）を削除
- [x] `PageSerializer` の `picture` を read_only にする
- [x] テスト更新: `wisme/tests/test_page_api.py`
  - `test_upload_picture_with_chapters_as_json_string` を「JSON で作成 → picture エンドポイントにアップロード」の2段階テストに置き換え
  - 画像の差し替え・削除
  - 他人のページへの画像アップロードが404
  - `/pages/` への multipart 送信が415になる

### 影響

- #08（ページフォームUI）: 保存時に ① ページを JSON で送信 → await → ② 画像があれば返却 id で picture エンドポイントへ送信。② が失敗してもページは保存済み（画像は任意項目）なので、画像のみ再送できる UI にする
