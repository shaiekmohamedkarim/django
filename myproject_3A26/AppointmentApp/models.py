from django.db import models
from AccountApp.models import Doctor, Patient
# Create your models here.
class Appointment(models.Model):
    reason = models.TextField()
    prescription = models.FileField(
        blank=True,
        upload_to='prescriptions/',
    )
    class Status(models.TextChoices):
        PENDING = 'Pending',"En attente"
        CONFIRMED = 'Confirmed',"Confirmé"
        CANCELED = 'Canceled',"Annulé"
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING) 
    # status = models.CharField(max_length=10, choices=[ ("Pending", "En attente"),("Confirmed", "Confirmé"),          ("Canceled", "Annulé"),],default="Pending")       
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')