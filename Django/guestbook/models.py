from django.db import models

class Guestbook(models.Model):
    # 1. 제목: 글자 수 제한(100자)
    title = models.CharField(max_length=100)

    # 2. 작성자: 글자 수 제한(50자)
    author = models.CharField(max_length=50)
    
    # 3. 내용: 줄바꿈이 가능하고 글자 수 제한 없음
    content = models.TextField()
    
    # 4. 게시글 비밀번호: 삭제 시 검증용
    password = models.CharField(max_length=20)
    
    # 5. 작성 시간: 글이 생성될 때 자동으로 현재 시간이 저장되는 날짜/시간 필드
    created_at = models.DateTimeField(auto_now_add=True) 

    # 6. 시간 순 정렬
    class Meta:
        ordering = ['-created_at']

    # 관리자 페이지나 터미널에서 글 제목이 한눈에 보이게
    def __str__(self):
        return self.title