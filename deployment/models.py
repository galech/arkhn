import uuid
from django.conf import settings
from django.db import models
from kubernetes import client
from .utils import get_deployment_pods, apps_v1

class Deployment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    replicas = models.IntegerField(default=1)

    @property
    def pods(self):
        return get_deployment_pods(self)

    def create_k8s_deployment(self):

        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=str(self.pk)),
            spec=client.V1DeploymentSpec(
                replicas=self.replicas,
                selector=client.V1LabelSelector(match_labels={"app": str(self.pk)}),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": str(self.pk)}),
                    spec=client.V1PodSpec(containers=[client.V1Container(
                        name=self.label,
                        image=self.image,
                        ports=[client.V1ContainerPort(container_port=80)]
                    )])
                )
            )
        )
        return apps_v1.create_namespaced_deployment(namespace=settings.KUBE_NAMESPACE, body=deployment)


    def delete_k8s_deployment(self):

        apps_v1.delete_namespaced_deployment(
            name=str(self.pk),
            namespace=settings.KUBE_NAMESPACE,
            body=client.V1DeleteOptions(propagation_policy='Foreground')
        )

    def update_k8s_deployment(self, new_data):
        name = self.label
        body = {
            "spec": {
                "replicas": new_data.get("replicas", self.replicas),
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": name,
                                "image": new_data.get("image", self.image)
                            }
                        ]
                    }
                }
            }
        }

        apps_v1.patch_namespaced_deployment(
            name=name,
            namespace=settings.KUBE_NAMESPACE,
            body=body
        )