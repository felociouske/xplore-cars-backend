from django.contrib import admin
from .models import Car, CarImage, Enquiry, CarEnquiry

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'model', 'year', 'price', 'status')
    search_fields = ('name', 'make', 'model', 'year')
    list_filter = ('status', 'make', 'year')
    inlines = [CarImageInline]


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_at',)


@admin.register(CarEnquiry)
class CarEnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'model', 'email', 'created_at')
    search_fields = ('full_name', 'email', 'model')
    list_filter = ('created_at',)