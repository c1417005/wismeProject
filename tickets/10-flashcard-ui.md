# 10. フラッシュカード画面のReact化

## 背景・目的

`templates/wisme/flashcard.html` をReact化する。

既存仕様:
- 単語データはWord一覧と同じ
- カードUI: クリックすると裏返って意味が表示される
- 次/前のカードに移動
- ソート: 新着 / アルファベット

## 受け入れ基準（DoD）

- [ ] `features/flashcard/Flashcard.tsx`
- [ ] `useQuery(['words', sort])` を流用
- [ ] カード表面（word） / 裏面（meaning）のフリップアニメーション
- [ ] キーボードショートカット（← → でカード移動、Space でフリップ）あると◎
- [ ] カードがない時の空状態
- [ ] ソート切替
- [ ] ルート: `/r/flashcard`

## 作業手順

1. `Flashcard` コンポーネント（カード一覧をstateで管理、currentIndex）
2. CSS でフリップアニメーション（`transform: rotateY`）
3. キーバインド（任意）
4. ナビ追加

## 依存・優先度

- **依存**: #09
- **優先度**: 中
- **想定工数**: 0.5日
