# 07. ページ詳細画面のReact化

## 背景・目的

`templates/wisme/page_detail.html` + `_word_search_panel.html` をReact化する。読書メモの中核体験。

既存仕様:
- ページ基本情報（タイトル/日付/感想/サムネ）
- Chapter一覧（order順）
- そのページに紐づく単語一覧
- **単語検索パネル**: 入力 → Gemini APIで意味取得 → 表示。検索結果はそのページの単語として保存される
- 編集ボタン → `/wisme/page/{id}/update/`
- 削除ボタン → 確認画面

## 受け入れ基準（DoD）

- [ ] `features/pages/PageDetail.tsx`
- [ ] `useQuery(['pages', id], fetchPage)` で取得（chapters, words 含む）
- [ ] Chapter のタイトル+本文を順番に表示
- [ ] 単語パネル: 入力 → `POST /api/v1/words/search/` → 結果表示 + 一覧に追加（楽観的更新）
- [ ] 単語一覧（そのページ分）
- [ ] 編集ボタン → `/r/pages/:id/edit`
- [ ] 削除ボタン → 確認モーダル → `DELETE /api/v1/pages/:id/` → 一覧へ
- [ ] 404処理
- [ ] エラートースト/メッセージ表示

## 作業手順

1. 単語検索フック `useWordSearch` 作成
2. `PageDetail` コンポーネント
3. 単語パネルコンポーネント（再利用用に `WordSearchPanel`）
4. 削除確認モーダル
5. ルート登録

## 依存・優先度

- **依存**: #02, #03, #06
- **ブロックする**: #08
- **優先度**: 高
- **想定工数**: 0.5日

## 注意点

- 単語検索後、ページの単語一覧キャッシュを invalidate する（または楽観的更新）
- React Query の `setQueryData` で即時反映
