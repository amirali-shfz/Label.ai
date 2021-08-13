from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from label_ai.images import views

app_name = "Images"
urlpatterns = [
    path("all/", views.All_Endpoint.as_view()),
    path("confirmed/", views.Confirmed_Endpoint.as_view()),
    path("misclassified/", views.Misclassified_Endpoint.as_view()),
    path("discovered/", views.DiscoveredClassification_Endpoint.as_view()),
    path("controversial/", views.Controversial_Endpoint.as_view()),
    path("leastvotes/", views.LeastVotes_Endpoint.as_view()),
    path("prompt",views.ImageClassificationPrompt.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
