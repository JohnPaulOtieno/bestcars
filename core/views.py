from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Car, Testimonial, ContactInquiry


def home(request):
    featured_cars = Car.objects.filter(is_available=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    return render(request, 'core/home.html', {
        'featured_cars': featured_cars,
        'testimonials': testimonials,
    })


def available_units(request):
    cars = Car.objects.filter(is_available=True)
    make = request.GET.get('make', '')
    fuel = request.GET.get('fuel', '')
    transmission = request.GET.get('transmission', '')

    if make:
        cars = cars.filter(make__iexact=make)
    if fuel:
        cars = cars.filter(fuel_type=fuel)
    if transmission:
        cars = cars.filter(transmission=transmission)

    makes = Car.objects.filter(is_available=True).values_list('make', flat=True).distinct().order_by('make')
    return render(request, 'core/available_units.html', {
        'cars': cars,
        'makes': makes,
        'selected_make': make,
        'selected_fuel': fuel,
        'selected_transmission': transmission,
    })


def charges(request):
    return render(request, 'core/charges.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        car_interest = request.POST.get('car_interest', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and phone and message:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                car_interest=car_interest,
                message=message,
            )
            messages.success(request, 'Thank you! We will contact you within 24 hours.')
            return redirect('contact')

        messages.error(request, 'Please fill in all required fields.')

    return render(request, 'core/contact.html')
