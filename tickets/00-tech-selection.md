# 00. 技術選定とADR作成

## 背景・目的

React/DRFへの移行にあたり、ビルドツール・状態管理・認証方式などの主要な技術選定を先に確定させる。後工程のチケットで迷いを減らし、選定理由を `docs/adr/` に残すことで将来の見直しを容易にする。

ユーザーはRailsやReactの実務経験がないため、**学習コストが低く、情報量が多く、Djangoとの相性が良い**ものを優先する。

## 技術選定の提案

### ビルドツール
| 候補 | コメント |
|---|---|
| **Vite + React + TypeScript**（推奨） | 標準的・軽量・HMR高速。学習リソース豊富 |
| Next.js | SSR/SSG込みでオーバースペック。DRF併用前提だと旨味が薄い |
| Create React App | 非推奨化（メンテ停止） |

### 状態管理 / データ取得
| 候補 | コメント |
|---|---|
| **TanStack Query (React Query) + 必要に応じ Zustand**（推奨） | サーバー状態のキャッシュ・再取得が自動化されコード量が減る |
| Redux Toolkit | ボイラープレート多め。今回の規模だと過剰 |
| SWR | TanStack Queryで十分 |

### ルーティング
- **React Router v6**（推奨） … デファクト

### 認証方式（Django ↔ React）
| 候補 | コメント |
|---|---|
| **DRF SessionAuthentication + CSRF**（推奨） | allauthをそのまま使え、サーバーサイドCookieで安全。同一オリジン配信が前提 |
| TokenAuthentication / JWT | LocalStorageに置くとXSSリスク。allauthとの統合に追加実装が必要 |

→ Vite開発時は `/api/` を Django にプロキシ、本番は Django が `frontend/dist/` を WhiteNoise で配信する案を推奨。

### スタイル
- **CSS Modules または Tailwind CSS**（どちらかをチケット内で決定）
- 現状のCSSは `static/wisme/` 配下なので、移行ついでに整理

### フォルダ構成（提案）
```
frontend/
  src/
    api/         # APIクライアント (axios or fetch wrapper)
    components/  # 汎用コンポーネント
    features/    # 機能別 (pages, words, flashcard, profile)
    hooks/
    routes/      # ルーティング定義
    main.tsx
  vite.config.ts
  package.json
```

## 受け入れ基準（DoD）

- [ ] `docs/adr/0001-frontend-stack.md` を作成し、選定結果と理由を記載
- [ ] ビルドツール / 状態管理 / ルーティング / 認証方式 / スタイル の5項目を確定
- [ ] フロントエンドのフォルダ構成案を確定
- [ ] チーム（=ユーザー）レビュー済み

## 作業手順

1. 各候補のドキュメントを読み、本プロジェクト要件と照合
2. ADRドラフト作成
3. ユーザーレビュー
4. 確定版を `docs/adr/` にコミット

## 依存・優先度

- **依存**: なし（最初に着手）
- **優先度**: 高
- **想定工数**: 0.5日
