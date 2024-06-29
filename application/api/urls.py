from django.urls import re_path
from .views import ExamsTableView, ExamsFileView, ExamsEmptyView, DivsView, IndexView, EmplView

app_name = 'api'

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^empty/', ExamsEmptyView.as_view(), name='empty'),
    re_path(r'^exams/', ExamsTableView.as_view(), name='exams'),
    re_path(r'^api/file/', ExamsFileView.as_view(), name='file'),
    re_path(r'^divs/', DivsView.as_view(), name='divs'),
    re_path(r'^empls/', EmplView.as_view(), name='empls'),
]