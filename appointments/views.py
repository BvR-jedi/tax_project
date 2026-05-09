from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import AppointmentRequestForm


def home(request):
    return render(request, 'appointments/home.html')


def request_appointment(request):
    form = AppointmentRequestForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your appointment request has been received. We will review your preferred schedule and contact you soon.'
            )
            return redirect('request_success')

    return render(request, 'appointments/request_appointment.html', {'form': form})


def request_success(request):
    return render(request, 'appointments/success.html')
