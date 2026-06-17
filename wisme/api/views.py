from rest_framework.views import APIView
from rest_framework.response import Response


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
