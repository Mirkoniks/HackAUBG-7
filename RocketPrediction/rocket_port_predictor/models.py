from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class MissionInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rocket_name = models.CharField(max_length=100)
    launch_date = models.DateField()
    cost_million = models.FloatField()
    destination = models.CharField(max_length=100)
    launch_status = models.CharField(max_length=20, default='Success')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mission: {self.rocket_name} to {self.destination}"
