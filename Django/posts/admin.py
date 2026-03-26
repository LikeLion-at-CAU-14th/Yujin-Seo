# posts/admin.py
from django.contrib import admin
from .models import Post, Comment, Category
import random # 랜덤 닉네임 생성을 위해 random 모듈 임포트

# Post와 Category는 다대다 관계이므로, CategoryAdmin에서 PostInline을 사용하여 관리
class PostInline(admin.TabularInline):
    model = Post.categories.through
    extra = 1

# Category 관리자 설정
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]

# 댓글을 Post 안에 표시하는 Inline 설정
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # 기본으로 보여줄 빈 댓글 입력칸 개수

    # 관리자 페이지에서 보여줄 댓글 필드 설정
    fields = ('nickname', 'comment_id', 'content', 'likes_count', 'created_at', 'updated_at')

    # 수정 못하게 (읽기 전용)
    readonly_fields = ('nickname', 'comment_id', 'likes_count', 'created_at', 'updated_at')

    # writer는 자동으로 넣을 거니까 숨김
    exclude = ('writer',)

    # 연필(수정) 아이콘 제거
    show_change_link = False

    # 생성 시간 기준 정렬
    ordering = ('created_at',)

    # 댓글 ID 표시 메서드
    def comment_id(self, obj):
        return obj.id
    comment_id.short_description = 'ID'   

# Post 관리자 설정
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


    # 댓글 저장 시 writer 자동 입력
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in instances:
            if isinstance(obj, Comment):

                # writer 자동
                if not obj.writer:
                    obj.writer = request.user

                # 랜덤 이름 생성 
                names = ['익명토끼', '코딩고양이', '멋사사자', '졸린판다', '세션 과제하다가 울고 있는 익명의 누군가']
                if not hasattr(obj, 'nickname') or not obj.nickname:
                    obj.nickname = random.choice(names)

            obj.save()

        formset.save_m2m()

        # 댓글 저장 시 writer 자동 입력
        for obj in instances:
            # Comment일 때만 writer 자동 설정
            if isinstance(obj, Comment) and not obj.writer:
                obj.writer = request.user  # 현재 로그인한 관리자 계정

            obj.save()  # 저장

        formset.save_m2m()  # ManyToMany 있을 경우 저장

# admin 등록
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)