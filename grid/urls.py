from django.urls import path

from . import views

app_name = "grid"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("add/", views.add_project, name="add"),
    path("<int:pk>/", views.DisplayView.as_view(), name="display"),
]
