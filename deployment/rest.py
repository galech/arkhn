from rest_framework import viewsets
from rest_framework.pagination import CursorPagination

from deployment.models import Deployment

from .serializers import DeploymentSerializer


class DeploymentCursorPagination(CursorPagination):
    page_size = 1
    ordering = ("label", "id")


class DeploymentViewSet(viewsets.ModelViewSet):

    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    pagination_class = DeploymentCursorPagination
