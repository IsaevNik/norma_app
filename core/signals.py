from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Order


__all__ = ['pre_save_order_signal']


@receiver(pre_save, sender=Order)
def pre_save_order_signal(sender, instance, **kwargs):
    if not instance.id:
        return

    old_instance = sender.objects.get(pk=instance.pk)
    if old_instance.status != instance.status and instance.status == sender.DEPOSITED:
        instance.guest.generate_enter_code()
        instance.guest.send_success()

    elif old_instance.status != instance.status and instance.status == sender.DECLINED:
        instance.guest.send_fail()

