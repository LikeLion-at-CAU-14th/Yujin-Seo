# posts/models.py
from django.db import models
from accounts.models import User

# 추상 클래스 정의
class BaseModel(models.Model): # models.Model을 상속받음
    created_at = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
    updated_at = models.DateTimeField(auto_now=True) # 객체를 저장할 때 날짜와 시간 갱신

    class Meta:
        abstract = True

# Category 모델 정의
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Post 모델 정의
class Post(BaseModel): # BaseModel을 상속받음

    CHOICES = (
        ('STORED', '보관'),
        ('PUBLISHED', '발행')
    )

    title = models.CharField(max_length=50)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=CHOICES, default='STORED')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    categories = models.ManyToManyField(Category, related_name='posts')

    def __str__(self):
        return self.title

# Comment 모델 정의
class Comment(BaseModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    writer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )

    content = models.TextField()

    likes_count = models.PositiveIntegerField(default=0)

    nickname = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.content[:20]