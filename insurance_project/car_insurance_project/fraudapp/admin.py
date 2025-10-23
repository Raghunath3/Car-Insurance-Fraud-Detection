from django.contrib import admin
from .models import Prediction
from .models import Contact

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'prediction', 'fraud_probability', 'threshold', 'payout', 'created_at')
    list_filter = ('prediction', 'created_at')
    search_fields = ('credit_score', 'age', 'premium')

    

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')

