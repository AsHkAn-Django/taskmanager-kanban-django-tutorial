from django.db import models


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=264)
    is_complete = models.BooleanField(default=False)
    order = models.PositiveBigIntegerField(null=True, blank=False)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.order is None:
            self.order = self.pk
            super().save(update_fields=['order'])
            
        return super().save(*args, **kwargs)
