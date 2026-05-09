from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'email',
        'preferred_date',
        'preferred_time',
        'status',
        'created_at',
    ]
    list_filter = ['status', 'preferred_date', 'created_at']
    search_fields = ['full_name', 'email', 'phone_number']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']

    fieldsets = (
        ('Client information', {
            'fields': [
                'full_name',
                'email',
                'phone_number',
                'client_notes',
            ]
        }),
        ('Appointment details', {
            'fields': [
                'preferred_date',
                'preferred_time',
                'status',
                'finalized_datetime',
                'internal_notes',
            ]
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    )
