from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Patient, Doctor, Appointment

@admin.register(Patient)
class PatientAdmin(UserAdmin):
    model = Patient
    list_display = ('username', 'email','age','gender', 'is_staff', 'is_active','password')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    delete_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'specialty', 'city', 'experience_years', 'clinic_address', 'password')
    search_fields = ('name', 'email', 'specialty', 'city')

@admin.register(Appointment)  # Register the Appointment model
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    search_fields = ('patient__username', 'doctor__name', 'date')
    list_filter = ('status',)
    ordering = ('-date', '-time')