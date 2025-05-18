from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Deployment


@receiver(pre_delete, sender=Deployment)
def cleanup_deployment(sender, instance: Deployment, **kwargs):
    instance.delete_k8s_deployment()

@receiver(post_save, sender=Deployment)
def post_save_handler(sender, instance: Deployment, created, **kwargs):
    if created:
        instance.create_k8s_deployment()
    else:
        instance.update_k8s_deployment()