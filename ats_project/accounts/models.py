from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Registration(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    checkBox = models.BooleanField(default=False)
    isHr = models.BooleanField(default=False)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} | {self.email}"
    
