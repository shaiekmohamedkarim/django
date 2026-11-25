from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from AccountApp.models import Doctor, Patient


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "En attente"
        CONFIRMED = "Confirmed", "Confirmé"
        CANCELLED = "Cancelled", "Annulé"

    reason = models.TextField()
    prescription = models.FileField(
        blank=True,
        upload_to="prescriptions/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")

    class Meta:
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
                violation_error_message="Ce médecin a déjà un rendez-vous à cette date.",
            )
        ]

    def clean(self):
        super().clean()
        if self.appointment_date is None:
            return

        date_was_changed = self._state.adding
        if not self._state.adding:
            previous_date = type(self).objects.filter(pk=self.pk).values_list(
                "appointment_date", flat=True
            ).first()
            date_was_changed = previous_date is not None and previous_date != self.appointment_date

        if date_was_changed and self.appointment_date <= timezone.now():
            raise ValidationError(
                {"appointment_date": "La date du rendez-vous doit être dans le futur."}
            )

    def __str__(self):
        return f"{self.doctor} — {self.patient} — {self.appointment_date:%Y-%m-%d %H:%M}"
