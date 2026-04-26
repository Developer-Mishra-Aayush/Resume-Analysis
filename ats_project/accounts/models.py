from django.db import models

# Create your models here.
class Registration(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    checkBox = models.BooleanField(default=False)
    isHr = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} | {self.email}"