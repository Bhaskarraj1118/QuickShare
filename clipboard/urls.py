
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('share/<uuid:share_id>/', views.share_clipboard, name='share_clipboard'),
]
