# posts/urls.py
from django.urls import path
from posts.views import *

# URL 패턴 정의
urlpatterns = [
    #path('', hello_world, name = 'hello_world'),
    #path('page', index, name='my-page'),
    #path('<int:id>', get_post_detail),

    #path('', PostList, name = "post_list"), # Post 생성, 전체 조회
    #path('<int:post_id>/', post_detail, name = "post_detail"), # Post 단일조회, 수정, 삭제
    #path('<int:post_id>/comments/', comment_list, name = "comment_list") # Comment 생성, 전체 조회

    path('', PostList.as_view()),                                     # 게시글 전체 조회 및 생성
    path('<int:post_id>/', PostDetail.as_view()),                    # 게시글 개별 조회, 수정, 삭제

    # Comment 관련 URL (계층 구조 반영)
    path('<int:post_id>/comments/', CommentList.as_view()),          # 특정 게시글의 댓글 목록 및 생성
    path('<int:post_id>/comments/<int:comment_id>/', CommentDetail.as_view()), # 특정 게시글의 특정 댓글 상세/수정/삭제
    ]