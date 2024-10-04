
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ShippingAddress

User = get_user_model()

@receiver(post_save, sender=User)
def create_default_shipping_address(sender, instance, created, **kwargs):
    """
    Create a default shipping address for a newly created user if one doesn't exist.
    
    Args:
        sender (type): The sender of the signal (not used in this function).
        instance (User): The User instance that was just created.
        created (bool): A boolean indicating if the User instance was created.
        **kwargs: Additional keyword arguments passed to the function.
    
    Returns:
        None: This function doesn't return anything.
    """
    if created:
        if not ShippingAddress.objects.filter(user=instance).exists():
            ShippingAddress.create_default_shipping_address(user=instance)