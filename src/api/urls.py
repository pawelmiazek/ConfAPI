from django.urls import path

from .views import ConfiguratorView


urlpatterns = [
    path("configurator/", ConfiguratorView.as_view()),
]
