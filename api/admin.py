from django.contrib import admin
from .models import Car, CarImage, CarEnquiry, ContactEnquiry, Testimonial
from markdownx.admin import MarkdownxModelAdmin


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(MarkdownxModelAdmin):
    list_display = ('make', 'model', 'year', 'price_from', 'price_to', 'status', 'created_at')
    search_fields = ('name', 'make', 'model')
    list_filter = ('status', 'make', 'year', 'engine_type')
    inlines = [CarImageInline]


@admin.register(CarEnquiry)
class CarEnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vehicle_of_interest', 'budget_range', 'phone', 'email', 'created_at')
    search_fields = ('full_name', 'email', 'vehicle_of_interest')
    list_filter = ('budget_range', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject_type', 'subject', 'email', 'phone', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('subject_type', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author_name', 'author_role', 'layout_type',
        'rating', 'featured', 'show_on_homepage', 'display_order', 'created_at',
    )
    list_editable = ('featured', 'show_on_homepage', 'display_order')
    list_filter = ('layout_type', 'featured', 'show_on_homepage', 'rating')
    search_fields = ('title', 'author_name', 'testimonial_text')
    ordering = ('display_order', '-created_at')
    readonly_fields = ('created_at', 'updated_at', 'slug', 'youtube_id')

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'slug',
                ('author_name', 'author_role'),
            )
        }),
        ('Content', {
            'fields': (
                'testimonial_text',
                ('youtube_url', 'layout_type'),
            ),
            'description': 'Add a text testimonial, YouTube link, or both depending on layout type.'
        }),
        ('Display Settings', {
            'fields': (
                'rating',
                'featured',
                'show_on_homepage',
                'display_order',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )