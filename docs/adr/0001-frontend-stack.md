# ADR 0001: フロントエンド技術スタックの選定

- ステータス: 承認済み
- 日付: 2026-06-18
- 関連チケット: [00-tech-selection](../../tickets/00-tech-selection.md)

## コンテキスト

Wisme を現状の Django テンプレート（MPA）構成から、**Django (DRF) API サーバー + React SPA** 構成へ段階的に移行する。後工程の各チケットで判断が割れないよう、主要な技術選定（ビルドツール / 状態管理 / ルーティング / 認証方式 / スタイル）を本 ADR で先に確定させる。

選定の前提となるプロジェクトの実態:

- 認証は **django-allauth**（セッション Cookie + メール認証 + Google OAuth）が既に稼働中
- 既存 CSS 資産は `static/wisme/css/style.css` 57 行 + `normalize.css` のみと小規模
- React 化対象は約 11 画面の小〜中規模
- 本番は Heroku + WhiteNoise で、フロントとバックを同一オリジン配信可能
- 開発者（ユーザー）は React/Rails の実務未経験 → **学習コスト・情報量を最優先**
- 段階的移行のため、既存テンプレート版を壊さず併設で進める

## 決定

| 項目 | 採用 |
|---|---|
| ビルドツール | **Vite + React + TypeScript** |
| 状態管理 / データ取得 | **TanStack Query**（クライアント状態が増えたら Zustand を追加） |
| ルーティング | **React Router** |
| 認証方式 | **DRF SessionAuthentication + CSRF** |
| スタイル | **Tailwind CSS** |

### フォルダ構成

```
frontend/
  src/
    api/         # APIクライアント（fetch/axios ラッパ）
    components/  # 汎用UIコンポーネント
    features/    # 機能別（pages, words, flashcard, profile）
    hooks/       # 再利用ロジック
    routes/      # ルーティング定義
    main.tsx
  vite.config.ts
  package.json
```

### 配信方針

- 開発時: Vite の dev サーバーが `/api/` へのリクエストを Django にプロキシする
- 本番: Django が `frontend/dist/` のビルド成果物を WhiteNoise で同一オリジン配信する

## 選定理由

### ビルドツール: Vite + React + TypeScript

- API 供給は DRF が担うため、フロントは純粋な SPA で十分。Next.js の SSR 機能は本構成では Django と役割が重複し、学習コストだけ増えるため不採用。
- Create React App は公式に非推奨・メンテ停止のため不採用。
- Vite は起動・HMR が高速で設定が最小限、学習リソースが最も豊富。
- TypeScript は API レスポンスの型定義とコンパイル時チェックで初学者のミスを減らし、長期保守にも効く。

### 状態管理: TanStack Query

- アプリの状態の大半は「サーバー由来のデータ（ページ一覧・単語帳など）」= サーバー状態であり、TanStack Query が得意とする領域。キャッシュ・再取得・ローディング/エラー管理が自動化され、コード量が減る。
- 既存 `WordService` の DB キャッシュ方針とも相性が良い。
- Redux Toolkit はボイラープレートが多く 11 画面規模には過剰。SWR は機能・情報量で一歩劣る。
- クライアント状態（モーダル開閉、フラッシュカードの現在位置など）が増えた時点で Zustand を追加導入する。

### ルーティング: React Router

- SPA ルーティングのデファクトスタンダードで、情報量・安定性が最大。初学者に優しい。

### 認証方式: DRF SessionAuthentication + CSRF

- 既に allauth がセッション認証で稼働しており、メール認証・Google OAuth も完成済み。**JWT を選ぶとこれらの資産を捨てて再実装が必要**になる。
- セッション Cookie は HttpOnly で XSS に強い。JWT を LocalStorage に置く方式は XSS でのトークン漏洩リスクがある。
- 同一オリジン配信を前提とすれば Cookie がそのまま効き、追加実装がほぼ不要。CORS 設定も最小限で済む。

### スタイル: Tailwind CSS

- 既存 CSS 資産が 57 行と小規模なため、どの方式でも移行負担は軽い。
- ユーティリティクラスによる高速な開発とデザインの一貫性を重視して Tailwind を採用。Vite との統合も容易。
- CSS Modules（素の CSS 知識で書ける）も有力な対抗馬だったが、開発速度・一貫性・情報量を優先した。

## 検討した代替案

| 項目 | 代替案 | 不採用の理由 |
|---|---|---|
| ビルド | Next.js | DRF と役割が重複しオーバースペック、学習範囲が広い |
| ビルド | Create React App | 公式に非推奨・メンテ停止 |
| 状態管理 | Redux Toolkit | ボイラープレートが多く本規模では過剰 |
| 状態管理 | SWR | TanStack Query で十分、情報量で一歩劣る |
| ルーティング | TanStack Router | 新しく情報が少なく初学者には時期尚早 |
| 認証 | Token / JWT | LocalStorage 保管の XSS リスク、allauth 統合に追加実装が必要 |
| スタイル | CSS Modules | 開発速度・一貫性・情報量で Tailwind を優先 |

## 結果・影響

- 後続チケット 01（DRF 基盤導入）は SessionAuthentication + CSRF + 同一オリジン配信を前提に設計する。
- チケット 05（React 基盤）は Vite + React + TypeScript + TanStack Query + React Router + Tailwind CSS でセットアップする。
- 既存の Django テンプレート版は移行完了（チケット 13）まで残し、double-write で本番を壊さず進める。
