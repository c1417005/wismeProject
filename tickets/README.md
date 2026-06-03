# React + DRF 移行チケット一覧

## ゴール

現状のDjangoテンプレートMPA構成から、**Django (DRF) APIサーバー + React SPA** 構成へ段階的に移行する。

- **移行戦略**: 段階的移行（既存DjangoテンプレートとReact/DRFを併設し、画面単位で置き換え）
- **本番（Heroku）を壊さずに進める**ことを優先

## 依存関係

```
00 技術選定
  └─ 01 DRF基盤導入
       ├─ 02 Page API
       ├─ 03 単語API
       └─ 04 その他API
            └─ 05 Reactプロジェクト基盤
                 ├─ 06 ページ一覧 UI
                 │    └─ 07 ページ詳細 UI
                 │         └─ 08 ページ作成/編集 UI
                 ├─ 09 単語一覧 UI
                 │    └─ 10 フラッシュカード UI
                 ├─ 11 プロフィール UI
                 └─ 12 ダッシュボード+フィードバック UI
                      └─ 13 旧テンプレート削除/ドキュメント整備
```

## チケット一覧

| # | タイトル | 優先度 | 想定工数 |
|---|---|---|---|
| 00 | [技術選定とADR作成](00-tech-selection.md) | 高 | 0.5日 |
| 01 | [DRF基盤導入と認証/CORS設定](01-drf-setup.md) | 高 | 1日 |
| 02 | [Page/Chapter API実装](02-page-api.md) | 高 | 1日 |
| 03 | [単語検索/単語帳 API実装](03-word-api.md) | 高 | 0.5日 |
| 04 | [BookThumbnail/Feedback/Profile API実装](04-misc-api.md) | 中 | 0.5日 |
| 05 | [Reactプロジェクト基盤セットアップ](05-react-foundation.md) | 高 | 1日 |
| 06 | [ページ一覧画面のReact化](06-page-list-ui.md) | 高 | 0.5日 |
| 07 | [ページ詳細画面のReact化](07-page-detail-ui.md) | 高 | 0.5日 |
| 08 | [ページ作成/編集画面のReact化](08-page-form-ui.md) | 高 | 1日 |
| 09 | [単語一覧画面のReact化](09-word-list-ui.md) | 中 | 0.5日 |
| 10 | [フラッシュカード画面のReact化](10-flashcard-ui.md) | 中 | 0.5日 |
| 11 | [プロフィール画面のReact化](11-profile-ui.md) | 低 | 0.5日 |
| 12 | [ダッシュボード/フィードバックのReact化](12-dashboard-ui.md) | 低 | 0.5日 |
| 13 | [旧テンプレート削除とドキュメント整備](13-cleanup.md) | 低 | 0.5日 |

合計: 約8〜9日（学習時間含むと2〜3週間程度を想定）

## スコープ外（今回の移行では扱わない）

- 認証画面（allauthテンプレート）の置き換え … ハイブリッド方針で当面そのまま
- 管理画面（Django Admin）
- i18n切り替え機構のReact側統合（必要になった時点で別チケット化）

## 進め方のメモ

- 各チケットは feature ブランチ単位で進める想定
- API実装時、既存テンプレート版は **壊さない**（旧URLを残してdouble-write）
- React化は1画面ずつ本番リリース可能な単位でマージしていく
