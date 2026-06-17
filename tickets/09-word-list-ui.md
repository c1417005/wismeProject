# 09. 単語一覧画面のReact化

## 背景・目的

`templates/wisme/word_list.html` をReact化する。

既存仕様:
- 自分の単語一覧
- ソート: 新着 / アルファベット順（`?sort=alpha`）
- 各単語: word, meaning, 関連ノート（あれば）
- 削除ボタン（論理削除）

## 受け入れ基準（DoD）

- [ ] `features/words/WordList.tsx`
- [ ] `useQuery(['words', sort])` で取得、sortパラメータで再取得
- [ ] ソート切り替えUI（タブ or セレクト）
- [ ] 削除ボタン → `DELETE /api/v1/words/:id/` → 一覧から消える
- [ ] 関連ノートのタイトル表示（クリックで詳細画面へ）
- [ ] 空状態
- [ ] ルート: `/r/words`

## 作業手順

1. APIクライアントに `fetchWords(sort)`, `deleteWord(id)` 追加
2. `WordList` コンポーネント
3. ルート登録 + ナビ追加

## 依存・優先度

- **依存**: #03, #05
- **ブロックする**: #10
- **優先度**: 中
- **想定工数**: 0.5日
