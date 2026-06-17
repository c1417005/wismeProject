# 05. Reactプロジェクト基盤セットアップ

## 背景・目的

Reactフロントエンドの土台を構築する。後続のUIチケットがすぐ実装に入れる状態にする。

## 提案する構成

```
frontend/
  src/
    api/
      client.ts          # fetchラッパー（CSRF/エラーハンドリング）
      pages.ts           # Page系API呼び出し
      words.ts
      ...
    components/
      Layout.tsx
      Header.tsx
      ProtectedRoute.tsx
    features/
      pages/
      words/
      flashcard/
      profile/
      dashboard/
    hooks/
    routes/
      index.tsx          # React Router定義
    main.tsx
    App.tsx
  index.html
  vite.config.ts
  package.json
  tsconfig.json
```

## 受け入れ基準（DoD）

- [ ] `frontend/` ディレクトリに Vite + React + TypeScript プロジェクト初期化
- [ ] 依存: `react-router-dom`, `@tanstack/react-query`, `axios` または `fetch` ベースクライアント
- [ ] `vite.config.ts` で `/api` を `http://localhost:8000` にプロキシ
- [ ] APIクライアントが CSRFトークン（`csrftoken` Cookie）を `X-CSRFToken` ヘッダに自動付与
- [ ] `QueryClientProvider` を App ルートに設置
- [ ] React Router の基本構成（`/r/pages`, `/r/words`, `/r/profile` 等のプレフィックスで一旦本番と分離）
- [ ] `ProtectedRoute` … 未認証時は `/accounts/login/` にリダイレクト
- [ ] 共通レイアウト `<Header>` + `<Outlet>`
- [ ] Django側で `frontend/dist/` を配信する設定（または開発時はVite単独）
  - 本番: `collectstatic` で WhiteNoise が配信できるよう Vite の `build.outDir` を `staticfiles_src/react/` 等に設定
- [ ] サンプル画面（"Hello Wisme" + `/api/v1/health/` 呼び出し結果表示）が動く
- [ ] `README.md` または `frontend/README.md` に dev/build 手順を記載

## 作業手順

1. `npm create vite@latest frontend -- --template react-ts`
2. ルーター/Query/APIクライアント導入
3. Viteプロキシ設定
4. CSRF対応のfetchラッパー作成（`getCookie('csrftoken')` → ヘッダ付与）
5. ProtectedRoute / Layout
6. サンプル画面動作確認
7. ビルド成果物のDjango配信設定（本番準備）
8. CI（あれば）にnpm buildステップ追加

## 依存・優先度

- **依存**: #00, #01, #02, #03, #04（API側が一通り揃ってから着手すると統合確認がスムーズ）
- **ブロックする**: #06〜#12 全部
- **優先度**: 高
- **想定工数**: 1日

## 注意点

- 開発時のオリジン違い（Vite: 5173, Django: 8000）でCSRF/CORSが噛み合うよう、`#01` で設定済みのCORS_ALLOWED_ORIGINSを確認
- 本番は同一オリジン配信を推奨（CSRF設定が単純になる）
- React側のルートは当面 `/r/` 配下に分けることで、既存のテンプレ版と共存可能（移行完了後に `/r/` を外す）
