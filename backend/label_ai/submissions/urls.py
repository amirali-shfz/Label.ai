from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from label_ai.submissions import views

app_name = "submissions"
urlpatterns = [
    path("", views.SubmissionList.as_view()),
    path("insert", views.SubmissionInsert.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
