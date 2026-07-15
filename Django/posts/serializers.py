### Model Serializer case

from rest_framework import serializers
from .models import Post, Comment
from config.custom_api_exceptions import PostConflictException
from django.utils import timezone

class PostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post    # serializer가 어떤 모델을 기반으로 만들어지는지 >> post
    fields = "__all__"  # 모델에서 어떤 필드를 가져올지 >> 전체 필드
    read_only_fields = ['writer', 'categories']  

  # 중복된 게시글 제목이 있다면 예외 발생
  def validate(self, data):
    if Post.objects.filter(title=data['title']).exists():
      raise PostConflictException(detail=f"A post with title: '{data['title']}' already exists.")
    
    return data
  
  #게시글은 하루에 하나만 올릴 수 있도록 예외 처리
  def validate(self, data):
    request = self.context.get('request')
    user = request.user
    today = timezone.now().date()
    today_posts_count = Post.objects.filter(writer=user, created_at__date=today).count()
    if today_posts_count >= 1:
      raise serializers.ValidationError("You can only create one post per day.")
  
    return data
  
  
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['post']

    # def validate(self, data):
    #   # 댓글을 최소 15자 이상 작성하도록 유효성 검사
    #   content = data.get('content', '')
    #   if len(content) < 15:
    #     raise serializers.ValidationError("Comment must be at least 15 characters long.")
    #   return data
    
    def validate_content(self, value):
        if len(value) < 15:
            raise serializers.ValidationError("Comment must be at least 15 characters long.")
        return value

from .models import Image
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"