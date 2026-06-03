# 06. ページ一覧画面のReact化

## 背景・目的

`templates/wisme/page_list.html` をReactに置き換える。最もシンプルな画面でReact化の動作確認を兼ねる。

既存仕様:
- 自分のページ一覧
- `page_date` 降順
- 各カードに `title`, `page_date`, サムネイル（`picture` か `image_url`）
- クリックで詳細画面遷移

## 受け入れ基準（DoD）

- [ ] `features/pages/PageList.tsx` を実装
- [ ] `useQuery(['pages'], fetchPages)` で `/api/v1/pages/` から取得
- [ ] ローディング/エラー/空状態のUI
- [ ] サムネイル表示（`picture.url` または `image_url`）。両方なしの場合はプレースホルダ
- [ ] 各カードクリックで `/r/pages/:id` に遷移
- [ ] ページネーション対応（無限スクロール or ボタン式、どちらか）
- [ ] 既存テンプレート版（`/wisme/page/list/`）はそのまま残す
- [ ] スクリーンショットで見た目の同等性を確認

## 作業手順

1. APIクライアントに `fetchPages(params)` 追加
2. `PageList` コンポーネント作成
3. ルートに登録（`/r/pages`）
4. ナビゲーション（ヘッダー）から到達可能に
5. 動作確認（dev server）

## 依存・優先度

- **依存**: #02, #05
- **ブロックする**: #07
- **優先度**: 高
- **想定工数**: 0.5日
