# 08. ページ作成/編集画面のReact化

## 背景・目的

`templates/wisme/page_form.html` と `page_update.html` をReact化する。最も実装が重い画面。

既存仕様:
- タイトル / 日付 / 感想 / 画像（picture もしくは image_url）
- **書籍サムネ検索**: タイトル+著者を入力 → Google Books から候補リストを取得 → 1つ選ぶと `image_url` にセット
- **Chapter動的フォーム**:
  - 「章を追加」ボタンで行追加
  - 各章: title (任意) + content
  - 行ごとに削除ボタン
  - 並び順は `order` フィールドで管理（hidden）
- 保存時、未紐付け（`note=None`）の検索済単語が自動でこのページに関連付け（#02 でAPI実装済み）

## 受け入れ基準（DoD）

- [ ] `features/pages/PageForm.tsx`（create/update 兼用）
- [ ] フォーム管理は React Hook Form 推奨（または素のuseState）
- [ ] Chapter は配列で持ち、追加/削除/並び替え対応（最低限 上下移動 or drag&drop）
- [ ] 画像アップロード: ファイル選択 → multipart 送信
- [ ] 書籍サムネ検索: `GET /api/v1/books/thumbnails/?title=&author=` → 候補グリッド → 選択で `image_url` に反映
- [ ] バリデーション（タイトル/日付必須）
- [ ] 保存成功 → 詳細画面へリダイレクト
- [ ] 保存失敗時のエラー表示
- [ ] 編集時、既存値が読み込まれる
- [ ] 既存テンプレート版は残す

## 作業手順

1. `PageForm` コンポーネント（mode: create | update）
2. `ChapterFieldArray` 子コンポーネント
3. `BookThumbnailPicker` 子コンポーネント
4. 画像アップロードUI（プレビュー付き）
5. APIクライアントに `createPage`, `updatePage`, `searchBookThumbnails` 追加
6. ルート: `/r/pages/new`, `/r/pages/:id/edit`

## 依存・優先度

- **依存**: #02, #04, #07
- **ブロックする**: #13
- **優先度**: 高
- **想定工数**: 1日

## 注意点

- Chapterの `order` はサーバー側で再採番するので、クライアントは配列インデックス順で送れば十分
- 画像のpictureとimage_urlの優先順位は既存挙動と合わせる（picture > image_url）
- react-hook-form の `useFieldArray` が並び替えに便利
