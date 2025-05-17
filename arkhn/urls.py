
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import routers

from deployment.rest import DeploymentViewSet

router = routers.DefaultRouter()
router.register(r'deployments', DeploymentViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
