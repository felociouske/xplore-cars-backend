from rest_framework import serializers
from .models import Car, CarImage, CarEnquiry, ContactEnquiry, Testimonial


class CarImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = CarImage
        fields = ['id', 'image']


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    price_display = serializers.SerializerMethodField()
    trim_levels_list = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id', 'name', 'make', 'model', 'year', 'grade', 'engine_type',
            'mileage', 'price_from', 'price_to', 'price_display', 'color',
            'description', 'transmission', 'features', 'status', 'created_at',
            'images', 'body_type', 'import_type', 'drive_side', 'trim_levels',
            'trim_levels_list',
        ]

    def get_price_display(self, obj):
        return obj.price_display()

    def get_trim_levels_list(self, obj):
        if not obj.trim_levels:
            return []
        return [t.strip() for t in obj.trim_levels.split(',') if t.strip()]


class CarEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarEnquiry
        fields = '__all__'


class ContactEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactEnquiry
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    youtube_embed_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = [
            'id', 'title', 'slug', 'author_name', 'author_role',
            'testimonial_text', 'youtube_url', 'youtube_id', 'youtube_embed_url',
            'layout_type', 'rating', 'featured', 'show_on_homepage',
            'display_order', 'created_at',
        ]

    def get_youtube_embed_url(self, obj):
        return obj.youtube_embed_url()