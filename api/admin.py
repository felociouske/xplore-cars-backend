from django.contrib import admin
from .models import Car, CarImage, CarEnquiry, ContactEnquiry, Testimonial, BlogPost


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm("api.add_carimage")

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm("api.change_carimage")

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm("api.delete_carimage")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "model", "year", "category", "body_type", "price_from", "price_to", "created_at")
    search_fields = ("name", "make", "model")
    list_filter = ("category", "body_type", "import_type", "make")
    inlines = [CarImageInline]

    fieldsets = (
        ("Identity", {
            "fields": (
                ("make", "model", "year"),
                "name",
                ("body_type", "import_type"),
                "category",
            ),
            "description": "Name is auto-filled from Make + Model + Year if left blank.",
        }),
        ("Trim & Variants", {
            "fields": ("trim_levels",),
            "description": "Enter comma-separated trim levels e.g. X, G, Moda, TRD Sportivo",
        }),
        ("Pricing", {
            "fields": (("price_from", "price_to"),),
            "description": "Price varies by trim, mileage, grading and year. Enter the full expected range.",
        }),
        ("Content", {
            "fields": ("features", "description"),
        }),
        ("YouTube Videos", {
            "fields": (
                ("youtube_video_1", "youtube_video_1_title"),
                ("youtube_video_2", "youtube_video_2_title"),
                ("youtube_video_3", "youtube_video_3_title"),
                ("youtube_video_4", "youtube_video_4_title"),
            ),
            "description": "Paste up to 4 YouTube URLs and add an optional title for each. Leave any slot blank if not needed.",
        }),
    )


@admin.register(CarEnquiry)
class CarEnquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "vehicle_of_interest", "budget_range", "phone", "email", "created_at")
    search_fields = ("full_name", "email", "vehicle_of_interest")
    list_filter = ("budget_range", "created_at")
    readonly_fields = ("created_at",)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "subject_type", "subject", "email", "phone", "created_at")
    search_fields = ("full_name", "email", "subject")
    list_filter = ("subject_type", "created_at")
    readonly_fields = ("created_at",)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "title", "author_name", "author_role", "layout_type",
        "rating", "featured", "show_on_homepage", "display_order", "created_at",
    )
    list_editable = ("featured", "show_on_homepage", "display_order")
    list_filter = ("layout_type", "featured", "show_on_homepage", "rating")
    search_fields = ("title", "author_name", "testimonial_text")
    ordering = ("display_order", "-created_at")
    readonly_fields = ("created_at", "updated_at", "slug", "youtube_id")

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                ("author_name", "author_role"),
            ),
        }),
        ("Content", {
            "fields": (
                "testimonial_text",
                ("youtube_url", "layout_type"),
            ),
            "description": "Add a text testimonial, YouTube link, or both depending on layout type.",
        }),
        ("Display Settings", {
            "fields": (
                "rating",
                "featured",
                "show_on_homepage",
                "display_order",
            ),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "published_at", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "subtitle", "content")
    readonly_fields = ("slug", "youtube_id", "created_at", "updated_at")
    list_editable = ("is_published",)

    fieldsets = (
        ("Post Identity", {
            "fields": ("title", "slug", "subtitle", "cover_image"),
        }),
        ("Content", {
            "fields": ("content",),
        }),
        ("YouTube (Optional)", {
            "fields": ("youtube_url", "youtube_id"),
            "description": "Paste a YouTube link to attach a video to this post.",
        }),
        ("Publishing", {
            "fields": ("author", "is_published", "published_at"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )