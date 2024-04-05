from django.urls import re_path
from .views import IndexView, ApiTableView, ApiFileView, ApiEmptyView

app_name = 'api'

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^empty/', ApiEmptyView.as_view()),
    re_path(r'^api/', ApiTableView.as_view()),
    re_path(r'^file/', ApiFileView.as_view(), name='file'),
]