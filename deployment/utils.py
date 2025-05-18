from django.conf import settings
from kubernetes import client, config

config.load_kube_config()

apps_v1 = client.AppsV1Api()
core_v1 = client.CoreV1Api()
MAX_LABEL_VALUES = 100


def get_deployment_pods(deployment):
    return get_deployments_pods([deployment])


def get_deployments_pods(deployments):
    apps_selector = [str(d.id) for d in deployments]
    chunks = [
        apps_selector[i: i + MAX_LABEL_VALUES]
        for i in range(0, len(apps_selector), MAX_LABEL_VALUES)
    ]
    return [
        pod
        for chunk in chunks
        for pod in core_v1.list_namespaced_pod(
            namespace=settings.KUBE_NAMESPACE,
            label_selector=f"app in ({','.join(chunk)})",
        ).items
    ]
