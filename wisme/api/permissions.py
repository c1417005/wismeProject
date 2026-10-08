"""API 用のカスタム権限クラス。"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """オブジェクトの `owner` がリクエストユーザーと一致する場合のみ許可する。

    各 ViewSet は `get_queryset` を owner で絞るため、他人のオブジェクトは
    通常そこで 404 になりこのクラスには到達しない。絞り込み漏れに対する
    二重の防御として、所有権のルールをビュー層にも明示しておく。
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id
