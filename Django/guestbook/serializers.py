from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from .models import Guestbook

class GuestbookSerializer(serializers.ModelSerializer):

    # 5개 중 하나 선택할 수 있도록 필드에 제한 두기
    character = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1
    )

    class Meta:
        model = Guestbook 
        
        fields = "__all__" # 모델의 모든 필드를 시리얼라이저에 포함
        read_only_fields = ['created_at'] # created_at 필드는 읽기 전용으로 설정하여, 클라이언트가 이 필드를 수정할 수 없도록 함