from rest_framework import serializers
from .models import Car, CarImage, CarEnquiry, ContactEnquiry, Testimonial


class CarImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = CarImage
        fields = ['id', 'image']


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'name', 'make', 'model', 'year', 'grade', 'engine_type',
            'mileage', 'price', 'color', 'description', 'transmission',
            'features', 'status', 'created_at', 'images'
        ]


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