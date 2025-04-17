from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import OrderLineItem
from bag.utils import save_bag_on_logout, restore_bag_on_login


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update or create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()


@receiver(user_logged_out)
def call_save_bag_on_logout(sender, request, user, **kwargs):
    """
    Save bag to current view before user logs out
    """
    save_bag_on_logout(request, user)


@receiver(user_logged_in)
def call_restore_bag_on_login(sender, request, user, **kwargs):
    """
    Restore bag after login
    """
    restore_bag_on_login(request, user)
