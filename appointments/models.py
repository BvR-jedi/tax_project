from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    finalized_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    client_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'preferred_date', 'preferred_time']

    def __str__(self):
        return f"{self.full_name} — {self.get_status_display()}"

    def clean(self):
        super().clean()

        if self.status == self.Status.CONFIRMED:
            if not self.finalized_datetime:
                raise ValidationError({
                    'finalized_datetime': 'Confirmed appointments must include a finalized date and time.'
                })

            duration = timedelta(hours=1)
            window_start = self.finalized_datetime - duration
            window_end = self.finalized_datetime + duration
            conflict_exists = Appointment.objects.filter(
                status=self.Status.CONFIRMED,
                finalized_datetime__isnull=False,
                finalized_datetime__gte=window_start,
                finalized_datetime__lt=window_end,
            ).exclude(pk=self.pk).exists()

            if conflict_exists:
                raise ValidationError(
                    'This finalized appointment overlaps with another confirmed appointment. Please choose a different time.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_pending(self):
        return self.status == self.Status.PENDING

    @property
    def is_confirmed(self):
        return self.status == self.Status.CONFIRMED

    @property
    def is_cancelled(self):
        return self.status == self.Status.CANCELLED

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

# Create your models here.
