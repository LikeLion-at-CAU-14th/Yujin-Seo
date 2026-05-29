from django.urls import path
from .views import GuestbookListCreateAPIView, GuestbookDetailAPIView

urlpatterns = [
    path('guestbooks/', GuestbookListCreateAPIView.as_view(), name='guestbook-list-create'),
    path('guestbooks/<int:pk>/', GuestbookDetailAPIView.as_view(), name='guestbook-detail'),
]