from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendshipInvitation, Notification

@receiver(post_save, sender=FriendshipInvitation)
def send_notification(sender, instance, created, **kwargs):
    if not created and instance.status == 'accepted':
        content = f"Your friendship invitation to {instance.to_user.username} has been accepted."
        Notification.objects.create(user=instance.from_user, content=content)