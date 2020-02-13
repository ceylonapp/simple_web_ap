from django.db import models


# Create your models here.

# Create your models here.
class FaqModel(models.Model):
    title = models.CharField(max_length=250)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)


# Create your models here.
class GuideLineModel(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
