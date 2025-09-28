from django.urls import path
from . import views
from .views import chat_api, stt_view, tts_view

urlpatterns = [
    path('', views.index, name='index'),
    path('chats/', views.chats, name='chats'),
    path('chat/', chat_api, name='chat_api'),
    path('stt/', stt_view, name='stt'),
    path('tts/', tts_view, name='tts'),
    path("automation/", views.automation_view, name="automation"),
]
