from django.db import models
from django.conf import settings


class Task(models.Model):
    name = models.CharField(max_length=264)
    is_complete = models.BooleanField(default=False)
    order = models.PositiveBigIntegerField(null=True, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new and self.order is None:
            super().save(*args, **kwargs)
            self.order = self.pk
            super().save(update_fields=['order'])
        else:
            super().save(*args, **kwargs)
