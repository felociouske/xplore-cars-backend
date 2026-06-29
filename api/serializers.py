from rest_framework import serializers
from .models import Car, CarImage, CarEnquiry, ContactEnquiry, Testimonial, BlogPost


class CarImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CarImage
        fields = ['id', 'image']

    def get_image(self, obj):
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return obj.image.url
        except Exception:
            return None
        return str(obj.image) if obj.image and isinstance(obj.image, str) else None


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    price_display = serializers.SerializerMethodField()
    trim_levels_list = serializers.SerializerMethodField()
    features_list = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id', 'name', 'make', 'model', 'year', 'category',
            'price_from', 'price_to', 'price_display',
            'description', 'features', 'features_list', 'created_at',
            'images', 'body_type', 'import_type',
            'trim_levels', 'trim_levels_list',
            'youtube_video_1', 'youtube_video_2',  # NEW
        ]

    def get_price_display(self, obj):
        return obj.price_display()

    def get_trim_levels_list(self, obj):
        if not obj.trim_levels:
            return []
        return [t.strip() for t in obj.trim_levels.split(',') if t.strip()]

    def get_features_list(self, obj):
        if not obj.features:
            return []
        return [f.strip() for f in obj.features.split('\n') if f.strip()]


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


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    youtube_embed_url = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'subtitle', 'cover_image_url',
            'content', 'author_name', 'youtube_url', 'youtube_id',
            'youtube_embed_url', 'is_published', 'published_at', 'created_at',
        ]

    def get_author_name(self, obj):
        if obj.author:
            full_name = obj.author.get_full_name()
            return full_name if full_name else obj.author.username
        return "Xplore Imports"

    def get_youtube_embed_url(self, obj):
        return obj.youtube_embed_url()

    def get_cover_image_url(self, obj):
        try:
            if obj.cover_image and hasattr(obj.cover_image, 'url'):
                return obj.cover_image.url
        except Exception:
            return None
        return None