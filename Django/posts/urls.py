# posts/urls.py
from django.urls import path
from posts.views import *

# URL 패턴 정의
urlpatterns = [
    #path('', hello_world, name = 'hello_world'),
    #path('page', index, name='my-page'),
    #path('<int:id>', get_post_detail),

    path('', post_list, name = "post_list"), # Post 생성, 전체 조회
    path('<int:post_id>/', post_detail, name = "post_detail"), # Post 단일조회, 수정, 삭제
    path('<int:post_id>/comments/', comment_list, name = "comment_list") # Comment 생성, 전체 조회
    ]