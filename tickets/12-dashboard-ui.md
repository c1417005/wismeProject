# 12. ダッシュボード/フィードバックのReact化

## 背景・目的

`templates/wisme/index.html` をReact化する。ログイン後のホーム画面。

既存仕様:
- ページ数の合計表示
- 最終更新ページへのリンク + 最終更新日時
- フィードバック送信フォーム（送信完了時 `?feedback=sent` でメッセージ表示）

## 受け入れ基準（DoD）

- [ ] `features/dashboard/Dashboard.tsx`
- [ ] `GET /api/v1/dashboard/` でカウントと最終ページ取得
- [ ] フィードバックフォーム（`POST /api/v1/feedback/`）
- [ ] 送信成功時のトースト or インラインメッセージ
- [ ] ルート: `/r/` （Reactアプリのトップ）
- [ ] LOGIN_REDIRECT_URL をReact側に向けるかどうかは #13 で判断

## 作業手順

1. APIクライアントに `fetchDashboard`, `submitFeedback` 追加
2. `Dashboard` コンポーネント + `FeedbackForm` 子コンポーネント
3. ルート登録

## 依存・優先度

- **依存**: #04, #05
- **ブロックする**: #13
- **優先度**: 低
- **想定工数**: 0.5日
