from collections import defaultdict

from django.db import models
from rest_framework import serializers

from .models import Deployment
from .utils import get_deployments_pods


class DeploymentListSerializer(serializers.ListSerializer):
    """To avoid n+1 call to kub api when serializing many instances"""

    def to_representation(self, data):

        if isinstance(data, (models.manager.BaseManager, models.query.QuerySet)):
            iterable = list(data.all())
        elif isinstance(data, list):
            iterable = data
        else:
            iterable = list(data)
        self.context["pods_by_deployment"] = defaultdict(list)
        for pod in get_deployments_pods(iterable):
            self.context["pods_by_deployment"][pod.metadata.labels["app"]].append(pod)

        return super().to_representation(iterable)


class DeploymentSerializer(serializers.ModelSerializer):

    pods = serializers.SerializerMethodField()

    class Meta:
        model = Deployment
        fields = "__all__"
        list_serializer_class = DeploymentListSerializer

    def get_pods(self, obj: Deployment):
        pods_by_deployment = self.context.get("pods_by_deployment", {})
        return [
            pod.to_dict()
            for pod in (
                pods_by_deployment[str(obj.pk)]
                if str(obj.pk) in pods_by_deployment
                else obj.pods
            )
        ]
