from django.urls import re_path
from .views import IndexView, ApiTableView, ApiFileView

urlpatterns = [
    re_path(r'^$', IndexView.as_view()),
    re_path(r'^api/', ApiTableView.as_view()),
    re_path(r'^file/', ApiFileView.as_view()),
]