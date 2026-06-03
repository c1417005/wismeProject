# 13. 旧テンプレート削除とドキュメント整備

## 背景・目的

全画面のReact化が完了した段階で、不要になった旧テンプレート/旧view/旧URLを削除し、ドキュメントを新構成に合わせて更新する。

## 受け入れ基準（DoD）

- [ ] 削除対象
  - `templates/wisme/*.html`（allauth/socialaccount系は残す）
  - `wisme/views.py` のテンプレート用クラスビュー（API以外）
  - `wisme/urls.py` のテンプレート用エントリ
  - `wisme/forms.py`（API利用ならSerializerに集約可。残すかは判断）
  - 旧 JavaScript（`static/wisme/` 配下に手書きJSがあれば）
- [ ] LOGIN_REDIRECT_URL を `/r/` に変更
- [ ] `config/urls.py` の `/wisme/` 配下を整理（必要なら丸ごと削除）
- [ ] `README.md` 更新
  - 技術スタック表に React / TanStack Query / Vite を追加
  - セットアップに `frontend/` の手順を追記
  - 「React + DRFへの移行を進める」セクションを「完了」記録に書き換え
- [ ] `CLAUDE.md` 更新（アーキテクチャ説明をAPI+SPA構成に書き換え）
- [ ] `docs/adr/0001-frontend-stack.md` を完了状態に更新（実装後の振り返り追記）
- [ ] テンプレ削除前にバックアップブランチ or タグを作成
- [ ] Heroku本番でも問題なく動作することを確認

## 作業手順

1. 全画面のReact版が安定動作することを確認（ユーザー受け入れテスト）
2. バックアップタグ作成 `git tag pre-spa-cleanup`
3. 削除対象を段階的に削除し、その都度デプロイで動作確認
4. ドキュメント更新
5. 不要な依存パッケージ（`django-encrypted-model-fields` は残す等）を見直し
6. 最終確認 + 本番デプロイ

## 依存・優先度

- **依存**: #06, #07, #08, #09, #10, #11, #12 すべて
- **優先度**: 低（最後）
- **想定工数**: 0.5日

## 注意点

- allauth系のテンプレート（login, signup 等）はハイブリッド方針なので **削除しない**
- 削除前に「これは本当に未使用か」をgrepで確認する
- 移行完了後、`/wisme/` の旧URLを残したまま `/r/` を撤去するか、`/r/` プレフィックスを `/` に統合するかは別途検討
