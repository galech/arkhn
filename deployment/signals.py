from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Deployment
from .utils import delete_k8s_deployment, create_k8s_deployment, update_k8s_deployment


@receiver(pre_delete, sender=Deployment)
def cleanup_deployment(sender, instance: Deployment, **kwargs):
    delete_k8s_deployment(instance)

@receiver(post_save, sender=Deployment)
def post_save_handler(sender, instance: Deployment, created, **kwargs):
    if created:
        create_k8s_deployment(instance)
    else:
        update_k8s_deployment(instance, {})