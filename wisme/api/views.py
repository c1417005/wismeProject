from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from wisme.api.permissions import IsOwner
from wisme.api.serializers import (
    PageDetailSerializer,
    PagePictureSerializer,
    PageSerializer,
)
from wisme.models import Page, SearchedWord


class HealthCheckView(APIView):
    """API 基盤の疎通確認用エンドポイント。

    ログイン済みユーザーには 200 を返す（未ログインは 403）。
    認証・権限のデフォルト設定（SessionAuthentication / IsAuthenticated）が
    効いていることの確認も兼ねる。
    """

    def get(self, request):
        return Response({
            'status': 'ok',
            'user': request.user.get_username(),
        })


class PageViewSet(viewsets.ModelViewSet):
    """読書メモ（Page）の CRUD。

    テンプレート版 `PageCreateView` / `PageUpdateView` と同じ挙動を保つ:

    - 自分が owner のページのみ対象（他人の UUID を直接指定すると 404）
    - 章は `chapters` のネスト書き込みで保存し、`order` はリスト順で再採番
    - 保存時に未関連の単語（`note=None`）をこのページへ自動で紐付ける
    - 一覧は `page_date` の降順（同日は作成日時の降順）
    - 本体は JSON のみ受け付け、表紙画像は `picture` アクションで別送する
    """

    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = [JSONParser]

    def get_queryset(self):
        return (
            Page.objects.filter(owner=self.request.user)
            .prefetch_related('chapters', 'words')
            .order_by('-page_date', '-created_at')
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PageDetailSerializer
        return PageSerializer

    def perform_create(self, serializer):
        page = serializer.save(owner=self.request.user)
        self._attach_unlinked_words(page)

    def perform_update(self, serializer):
        page = serializer.save()
        self._attach_unlinked_words(page)

    @action(
        detail=True,
        methods=['put', 'delete'],
        url_path='picture',
        parser_classes=[MultiPartParser],
    )
    def picture(self, request, pk=None):
        """表紙画像のアップロード／差し替え（PUT）と削除（DELETE）。

        ページ本体を JSON で保存した後、返却された id に対して画像だけを送る。
        `get_object()` 経由なので他人のページは 404 になる。
        差し替え・削除時は旧ファイルをストレージから消す。
        """
        page = self.get_object()

        if request.method == 'DELETE':
            if page.picture:
                page.picture.delete(save=False)
            page.picture = None
            page.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = PagePictureSerializer(page, data=request.data)
        serializer.is_valid(raise_exception=True)
        if page.picture:
            page.picture.delete(save=False)
        serializer.save()
        return Response(PageSerializer(page, context=self.get_serializer_context()).data)

    def _attach_unlinked_words(self, page):
        """まだどのページにも紐付いていない単語をこのページに関連付ける。

        テンプレート版（`PageCreateView` / `PageUpdateView`）からの移植。
        ただしテンプレート版は owner で絞っていないため他ユーザーの未関連単語まで
        巻き込む不具合があった。ここでは自分の単語だけを対象にする。
        """
        SearchedWord.objects.filter(
            note__isnull=True, owner=self.request.user
        ).update(note=page)
