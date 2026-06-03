# 11. プロフィール画面のReact化

## 背景・目的

`templates/wisme/profile.html` + `profile_update.html` をReact化する。

既存仕様:
- 表示名（display_name, 暗号化フィールド）
- プロフィール画像（Cloudinary）
- 編集画面で更新可能

## 受け入れ基準（DoD）

- [ ] `features/profile/Profile.tsx`（表示）
- [ ] `features/profile/ProfileEdit.tsx`（編集）
- [ ] `GET /api/v1/me/` で取得
- [ ] `PATCH /api/v1/me/`（multipart）で更新
- [ ] 画像プレビュー
- [ ] 編集→保存→表示画面に戻る
- [ ] ルート: `/r/profile`, `/r/profile/edit`

## 作業手順

1. APIクライアントに `fetchMe`, `updateMe` 追加
2. 表示/編集コンポーネント
3. ナビ追加

## 依存・優先度

- **依存**: #04, #05
- **優先度**: 低
- **想定工数**: 0.5日
