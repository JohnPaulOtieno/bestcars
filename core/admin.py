from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Testimonial, ContactInquiry


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'make', 'model', 'year', 'fuel_type', 'transmission', 'price_display', 'is_featured', 'is_available', 'created_at']
    list_filter = ['make', 'fuel_type', 'transmission', 'is_featured', 'is_available']
    search_fields = ['title', 'make', 'model', 'description']
    list_editable = ['is_featured', 'is_available']
    readonly_fields = ['created_at', 'car_image_preview']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'make', 'model', 'year', 'badge')
        }),
        ('Specs', {
            'fields': ('engine_cc', 'fuel_type', 'transmission', 'mileage')
        }),
        ('Pricing & Listing', {
            'fields': ('price', 'is_featured', 'is_available', 'description')
        }),
        ('Photo', {
            'fields': ('image', 'car_image_preview')
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def car_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px; border-radius:8px;" />', obj.image.url)
        return "No image uploaded"
    car_image_preview.short_description = "Preview"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'car_purchased', 'rating', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'rating']
    search_fields = ['name', 'car_purchased', 'quote']


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'car_interest', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'phone', 'car_interest']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'car_interest', 'message', 'created_at']

    def has_add_permission(self, request):
        return False


admin.site.site_header = "BestCars Admin"
admin.site.site_title = "BestCars"
admin.site.index_title = "Manage Your Listings"
