# myapp/models.py
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


class Upload(models.Model):
    salers_file = models.FileField(upload_to='uploads/')
    merch_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.uploaded_at:
            self.uploaded_at = timezone.now()
        super().save(*args, **kwargs)


@receiver(post_delete, sender=Upload)
def delete_files(sender, instance, **kwargs):
    instance.salers_file.delete(False)
    instance.merch_file.delete(False)
