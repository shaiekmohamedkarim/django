from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from AppointmentApp.admin import AppointmentInline

from .models import Doctor, Patient, Specialty, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Identité", {"fields": ("first_name", "last_name", "email")}),
    )


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Compte", {"fields": ("username", "first_name", "last_name", "email")}),
        ("Médecin", {"fields": ("license_number", "phone", "specialties")}),
    )
    list_display = ("last_name", "first_name", "license_number", "phone")
    list_filter = ("specialties",)
    search_fields = ("license_number", "last_name", "first_name")
    ordering = ("last_name",)
    filter_horizontal = ("specialties",)

    def get_readonly_fields(self, request, obj=None):
        return ("license_number",) if obj else ()


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Compte", {"fields": ("username", "first_name", "last_name", "email")}),
        ("Patient", {"fields": ("national_id", "phone", "birth_date")}),
    )
    list_display = ("last_name", "first_name", "national_id", "phone", "birth_date")
    search_fields = ("last_name", "first_name", "national_id")
    ordering = ("last_name",)
    inlines = [AppointmentInline]

    def get_readonly_fields(self, request, obj=None):
        return ("national_id",) if obj else ()
