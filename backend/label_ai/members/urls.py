from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from label_ai.members import views

app_name = "labels"
urlpatterns = [
    path("all", views.MemberList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)