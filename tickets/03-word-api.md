# 03. 単語検索/単語帳 API実装

## 背景・目的

AI単語検索（Gemini）と単語帳機能のAPIをDRFで提供する。

既存挙動の要点:
- `WordService.search_or_fetch(word, user)` … DB-cache-first。既に同じ単語があればGemini APIを呼ばずに返す
- `note=None` の `SearchedWord` は次のPage保存時に自動紐付け（→ #02 で実装）
- `WordDeleteView` は実際には削除せず `owner=None, note=None` で論理削除（他ユーザーが既に検索した単語データを残しキャッシュとして機能させる狙い）
- 一覧は `?sort=alpha` で語順ソート、それ以外は新着順

## 提案するエンドポイント

```
GET    /api/v1/words/                  自分の単語一覧（?sort=alpha|new、?page_id=で絞込）
POST   /api/v1/words/search/           単語検索 { "word": "..." } → { "id", "word", "meaning" }
                                       既存があれば即返却、なければGemini呼び出し
DELETE /api/v1/words/{id}/             論理削除（owner=None, note=None に更新）
```

## 受け入れ基準（DoD）

- [ ] `SearchedWordSerializer`（id, word, meaning, note_id, created_at）
- [ ] `WordViewSet` または FunctionView で上記3エンドポイントを実装
- [ ] `search` アクションは `WordService.search_or_fetch` を流用
- [ ] `destroy` を論理削除に上書き
- [ ] ソート: `?sort=alpha` → `word` 昇順、それ以外 → `created_at` 降順
- [ ] 既存テスト `WordSearchCacheTest` が引き続き通る
- [ ] テスト: `wisme/tests/test_word_api.py`
  - 新規単語検索でGeminiがモック呼び出される
  - 同じ単語で2回目はGeminiが呼ばれない
  - 他人の単語が一覧に出ない
  - 削除後、`owner=None, note=None` になっていること（DBレコードは残る）

## 作業手順

1. Serializer作成
2. ViewSet/Routing
3. `search` カスタムアクション実装（`@action(detail=False, methods=['post'])`）
4. destroy override
5. テスト

## 依存・優先度

- **依存**: #01
- **ブロックする**: #07（詳細画面の単語パネル）, #09, #10
- **優先度**: 高
- **想定工数**: 0.5日

## 注意点

- 既存テンプレート版の `page_return_mean` は GET なので URL/メソッドが変わる。テンプレ側を一時的に両対応にするか、テンプレ版はそのままGETで残し、React版だけPOSTに統一するか要検討
  - **推奨**: 既存GETエンドポイントは残し、新API（POST）を別途用意（破壊しない方針）
