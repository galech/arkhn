from rest_framework import serializers
from .models import Deployment

class DeploymentSerializer(serializers.ModelSerializer):

    pods = serializers.SerializerMethodField()

    class Meta:
        model = Deployment
        fields = '__all__'

    def get_pods(self, obj: Deployment):
        pods_by_deployment = self.context.get('pods_by_deployment', {})
        return [
            pod.to_dict() for pod in
            (pods_by_deployment[str(obj.pk)] if str(obj.pk) in pods_by_deployment else obj.pods)
        ]

