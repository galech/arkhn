from rest_framework import viewsets
from deployment.models import Deployment
from rest_framework.fields import empty
from django.db.models.query import QuerySet
from rest_framework.serializers import ListSerializer

from .serializers import DeploymentSerializer
from .utils import get_deployments_pods
from collections import defaultdict

class DeploymentViewSet(viewsets.ModelViewSet):

    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer


    def get_serializer(self, *args, **kwargs):
        ### To avoid n+1 queries to kub api
        serializer = super().get_serializer( *args, **kwargs)
        if isinstance(serializer, ListSerializer) and not hasattr(serializer, "initial_data"):
            if isinstance(serializer.instance, QuerySet):
                serializer.instance = list(serializer.instance)  # force evaluation to avoid missings instances
            serializer.context["pods_by_deployment"] = defaultdict(list)
            for pod in get_deployments_pods(serializer.instance):
                serializer.context["pods_by_deployment"][pod.metadata.labels["app"]].append(pod)
        return serializer
