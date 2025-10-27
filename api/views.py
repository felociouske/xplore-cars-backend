from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Car, CarImage, Enquiry, CarEnquiry, MasterclassEnquiry
from .serializers import (
    CarSerializer, CarImageSerializer,
    EnquirySerializer, CarEnquirySerializer, MasterclassEnquirySerializer
)

class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all().order_by('-created_at')
    serializer_class = CarSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['engine_type', 'status', 'year']
    search_fields = ['make', 'model', 'color', 'description']
    ordering_fields = ['price', 'year', 'mileage', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer


class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer
    http_method_names = ['post', 'get', 'head'] 

class CarEnquiryViewSet(viewsets.ModelViewSet):
    queryset = CarEnquiry.objects.all().order_by('-created_at')
    serializer_class = CarEnquirySerializer

class MasterclassEnquiryCreateView(viewsets.ModelViewSet):
    queryset = MasterclassEnquiry.objects.all()
    serializer_class = MasterclassEnquirySerializer