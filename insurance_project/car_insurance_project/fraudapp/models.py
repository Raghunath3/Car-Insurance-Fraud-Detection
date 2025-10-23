from django.db import models

# Create your models here.
from django.db import models

class Prediction(models.Model):
    credit_score = models.FloatField()
    age = models.IntegerField()
    experience = models.IntegerField()
    speeding = models.IntegerField()
    accidents = models.IntegerField()
    severity = models.IntegerField()
    gender = models.IntegerField()
    drunk = models.IntegerField()
    premium = models.FloatField()
    fraud_probability = models.FloatField()
    threshold = models.FloatField()
    prediction = models.CharField(max_length=20)
    payout = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} - ₹{self.payout}"
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

