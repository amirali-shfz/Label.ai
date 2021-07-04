from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from label_ai.classifications import views

app_name = "labels"
urlpatterns = [
    path("", views.ClassificationList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)