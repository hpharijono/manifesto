from django.db import models

# Create your models here.
class Value(models.Model):
    value = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.value


class Principle(models.Model):
    principle = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.principle

