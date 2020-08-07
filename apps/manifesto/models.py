from django.db import models

required = {
    'blank': False,
    'null': False
}


class Value(models.Model):
    value = models.CharField(max_length=250, **required)
    description = models.TextField()

    def __str__(self):
        return self.value


class Principle(models.Model):
    principle = models.CharField(max_length=250, **required)
    description = models.TextField()

    def __str__(self):
        return self.principle

