# posts/urls.py
from django.urls import path
from posts.views import *

# URL 패턴 정의
urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('page', index, name='my-page'),
        path('<int:id>', get_post_detail)

    ]