from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from label_ai.images import views

app_name = "Images"
urlpatterns = [
    path("all", views.ImageList.as_view()),
    path("mislabelled/", views.MisLabelledImages.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
