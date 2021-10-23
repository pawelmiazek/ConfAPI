from django.urls import include, path
from rest_framework import routers

from .views import ConfiguratorView


router = routers.DefaultRouter()

router.register("configurator", ConfiguratorView, basename="configurator")


urlpatterns = [
    path("", include(router.urls)),
]
