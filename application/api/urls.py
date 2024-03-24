from django.urls import re_path
from .views import IndexView, ApiView

urlpatterns = [
    re_path(r'^$', IndexView.as_view()),
    re_path(r'^api/', ApiView.as_view()),
]