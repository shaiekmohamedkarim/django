from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from .models import Appointment


class AppointmentStacked(admin.StackedInline):
    model = Appointment
    extra = 1
    fields = (
        "appointment_date",
        "doctor",
        "patient",
        "duration_minutes",
        "status",
        "reason",
        "prescription",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")


class DateRangeFilter(admin.SimpleListFilter):
    title = "date du rendez-vous"
    parameter_name = "date_range"

    def lookups(self, request, model_admin):
        return (
            ("today", "Aujourd'hui"),
            ("this_week", "Cette semaine"),
            ("upcoming", "À venir"),
        )

    def queryset(self, request, queryset):
        today = timezone.localdate()

        if self.value() == "today":
            return queryset.filter(appointment_date__date=today)

        if self.value() == "this_week":
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=7)
            return queryset.filter(
                appointment_date__date__gte=week_start,
                appointment_date__date__lt=week_end,
            )

        if self.value() == "upcoming":
            return queryset.filter(appointment_date__gt=timezone.now())

        return queryset


@admin.action(description="Confirmer les rendez-vous sélectionnés")
def confirm_appointments(modeladmin, request, queryset):
    queryset.update(status=Appointment.Status.CONFIRMED)


@admin.action(description="Annuler les rendez-vous sélectionnés")
def cancel_appointments(modeladmin, request, queryset):
    queryset.update(status=Appointment.Status.CANCELLED)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("appointment_date", "doctor", "patient", "duration_minutes", "status")
    list_editable = ("status",)
    list_filter = ("status", "doctor", DateRangeFilter)
    search_fields = (
        "patient__last_name",
        "patient__national_id",
        "doctor__last_name",
        "doctor__license_number",
    )
    ordering = ("-appointment_date",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Description", {"fields": ("reason", "status", "prescription")}),
        ("Date + Durée", {"fields": ("appointment_date", "duration_minutes")}),
        ("Patients / Médecins", {"fields": ("doctor", "patient")}),
        ("Planification", {"fields": ("created_at", "updated_at")}),
    )
    actions = (confirm_appointments, cancel_appointments)
