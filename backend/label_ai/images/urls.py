from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from label_ai.images import views

app_name = "Images"
urlpatterns = [
    path("confirmed/", views.ImagesByLabelView.as_view()),
    path("all", views.ImageListView.as_view()),
    path("mislabelled/", views.MisLabelledImagesView.as_view()),
    path("prompt",views.ImageClassificationPrompt.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
