"""API 用シリアライザ。

単語検索（03）・その他（04）のシリアライザは後続チケットで追加する。
"""
from rest_framework import serializers

from wisme.models import Page, Chapter, SearchedWord


class ChapterSerializer(serializers.ModelSerializer):
    """Page にネストされる章。

    `order` はクライアントから受け取った値ではなく、リスト内の並び順で
    サーバー側が再採番する（テンプレート版 `ChapterFormSet` と同じ挙動）。
    そのため書き込み時の `order` は無視され、レスポンスでは確定値を返す。
    """

    class Meta:
        model = Chapter
        fields = ['id', 'order', 'title', 'content']
        read_only_fields = ['id', 'order']


class WordSerializer(serializers.ModelSerializer):
    """Page 詳細に埋め込む単語（読み取り専用）。

    単語自体の CRUD は #03 で別途実装する。ここでは詳細表示用の最小限のみ。
    """

    class Meta:
        model = SearchedWord
        fields = ['id', 'word', 'meaning', 'created_at']
        read_only_fields = fields


class PageSerializer(serializers.ModelSerializer):
    """一覧・作成・更新で使う Page シリアライザ。

    `chapters` をネスト書き込み可能にしている。更新時に `chapters` が
    渡された場合は全置換（削除 → 並び順で再作成）し、追加・削除・並び替えを
    まとめて扱う。`chapters` を省略した PATCH では章を変更しない。
    `picture` は読み取り専用。アップロードは `PagePictureSerializer` で別送する。
    """

    chapters = ChapterSerializer(many=True, required=False)

    class Meta:
        model = Page
        fields = [
            'id', 'title', 'thoughts', 'page_date',
            'picture', 'image_url', 'chapters',
            'created_at', 'update_at',
        ]
        read_only_fields = ['id', 'picture', 'created_at', 'update_at']

    def create(self, validated_data):
        chapters_data = validated_data.pop('chapters', [])
        page = Page.objects.create(**validated_data)
        self._save_chapters(page, chapters_data)
        return page

    def update(self, instance, validated_data):
        chapters_data = validated_data.pop('chapters', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if chapters_data is not None:
            instance.chapters.all().delete()
            self._save_chapters(instance, chapters_data)
        return instance

    @staticmethod
    def _save_chapters(page, chapters_data):
        for idx, chapter_data in enumerate(chapters_data):
            chapter_data.pop('order', None)
            Chapter.objects.create(page=page, order=idx, **chapter_data)


class PagePictureSerializer(serializers.ModelSerializer):
    """表紙画像の単独アップロード用（`PUT /pages/{id}/picture/`）。"""

    picture = serializers.ImageField()

    class Meta:
        model = Page
        fields = ['picture']


class PageDetailSerializer(PageSerializer):
    """詳細表示用。chapters に加えて関連単語（words）を埋め込む。"""

    words = WordSerializer(many=True, read_only=True)

    class Meta(PageSerializer.Meta):
        fields = PageSerializer.Meta.fields + ['words']
