from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import SignupView, ChatView, IngestView, HistoryView

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('token', TokenObtainPairView.as_view(), name='token'),
    path('chat', ChatView.as_view(), name='chat'),
    path('ingest', IngestView.as_view(), name='ingest'),
    path('history', HistoryView.as_view(), name='history'),
]
