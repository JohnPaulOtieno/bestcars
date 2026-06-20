from django.db import models


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    title = models.CharField(max_length=200, help_text="e.g. 2022 Mazda CX-5 XD Turbo")
    make = models.CharField(max_length=100, help_text="e.g. Toyota, Mazda, Subaru")
    model = models.CharField(max_length=100, help_text="e.g. CX-5, Land Cruiser")
    year = models.PositiveIntegerField()
    engine_cc = models.PositiveIntegerField(help_text="Engine displacement in cc, e.g. 2500")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    mileage = models.PositiveIntegerField(help_text="Mileage in km")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='automatic')
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price in KES")
    badge = models.CharField(max_length=50, blank=True, help_text="e.g. 'New Arrival', 'Hot Deal'")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def price_display(self):
        return f"KES {self.price:,.0f}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, help_text="e.g. Nairobi, Mombasa")
    car_purchased = models.CharField(max_length=200, blank=True, help_text="e.g. 2021 Toyota RAV4")
    quote = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.name} — {self.car_purchased}"


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    car_interest = models.CharField(max_length=200, blank=True, help_text="e.g. Toyota Prado, budget ~3M")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} ({self.phone}) — {self.created_at.strftime('%d %b %Y')}"
