from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Car, CarImage, CarEnquiry, ContactEnquiry, Testimonial, BlogPost
from .serializers import (
    CarSerializer, CarImageSerializer,
    CarEnquirySerializer, ContactEnquirySerializer,
    TestimonialSerializer, BlogPostSerializer
)


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all().order_by('-created_at')
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['body_type', 'import_type']
    search_fields = ['name', 'description', 'features', 'body_type', 'import_type']
    ordering_fields = ['price_from', 'price_to', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price_from__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_from__lte=max_price)
        return queryset


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer


class CarEnquiryViewSet(viewsets.ModelViewSet):
    queryset = CarEnquiry.objects.all().order_by('-created_at')
    serializer_class = CarEnquirySerializer
    http_method_names = ['post', 'get', 'head']


class ContactEnquiryViewSet(viewsets.ModelViewSet):
    queryset = ContactEnquiry.objects.all().order_by('-created_at')
    serializer_class = ContactEnquirySerializer
    http_method_names = ['post', 'get', 'head']


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.order_by('display_order', '-created_at')

    def get_queryset(self):
        queryset = super().get_queryset()
        show_homepage = self.request.query_params.get('homepage')
        featured = self.request.query_params.get('featured')
        if show_homepage:
            queryset = queryset.filter(show_on_homepage=True)
        if featured:
            queryset = queryset.filter(featured=True)
        return queryset

    @action(detail=False, methods=['get'], url_path='homepage')
    def homepage_testimonials(self, request):
        testimonials = self.get_queryset().filter(show_on_homepage=True)
        serializer = self.get_serializer(testimonials, many=True)
        return Response(serializer.data)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_at', '-created_at')

    @action(detail=False, methods=['get'], url_path='recent')
    def recent_posts(self, request):
        posts = self.get_queryset()[:3]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)