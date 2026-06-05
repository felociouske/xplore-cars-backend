from rest_framework.routers import DefaultRouter
from .views import (
    CarViewSet, CarImageViewSet,
    CarEnquiryViewSet, ContactEnquiryViewSet,
    TestimonialViewSet, BlogPostViewSet,
)

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'car-images', CarImageViewSet)
router.register(r'car-enquiries', CarEnquiryViewSet)
router.register(r'contact-enquiries', ContactEnquiryViewSet)
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'blog', BlogPostViewSet, basename='blog')
urlpatterns = router.urls