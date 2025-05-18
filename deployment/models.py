import uuid

from django.conf import settings
from django.db import models
from kubernetes import client

from .utils import apps_v1, get_deployment_pods


class Deployment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    replicas = models.IntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=["label", "id"]),
        ]

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
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=self.label,
                                image=self.image,
                                ports=[client.V1ContainerPort(container_port=80)],
                            )
                        ]
                    ),
                ),
            ),
        )
        return apps_v1.create_namespaced_deployment(
            namespace=settings.KUBE_NAMESPACE, body=deployment
        )

    def delete_k8s_deployment(self):
        try:
            apps_v1.delete_namespaced_deployment(
                name=str(self.pk),
                namespace=settings.KUBE_NAMESPACE,
                body=client.V1DeleteOptions(propagation_policy="Foreground"),
            )
        except client.ApiException as e:
            if e.status == 404:
                pass
            else:
                raise

    def update_k8s_deployment(self):
        name = self.label
        body = {
            "spec": {
                "replicas": self.replicas,
                "template": {
                    "spec": {"containers": [{"name": self.label, "image": self.image}]}
                },
            }
        }

        apps_v1.patch_namespaced_deployment(
            name=name, namespace=settings.KUBE_NAMESPACE, body=body
        )
