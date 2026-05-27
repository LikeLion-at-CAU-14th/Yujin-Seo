# config/permissions.py
from rest_framework import permissions
from django.utils import timezone 

# 1. 통금 시간 체크 (오후 10시 ~ 오전 7시)
class IsNotCurfewTime(permissions.BasePermission):
    message = "현재 시간은 통금 시간입니다. 접근이 거부되었습니다."

    def has_permission(self, request, view):
        current_hour = timezone.localtime().hour
        
        if current_hour >= 22 or current_hour < 7:
            return False
        return True

# 2. 작성자 본인 확인 (수정/삭제 시)
class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "게시글의 작성자만 수정/삭제할 수 있습니다."

    def has_object_permission(self, request, view, obj):
        # GET 조회 등은 누구나 통과
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.writer == request.user