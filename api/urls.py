from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CarImageViewSet, EnquiryViewSet, CarEnquiryViewSet, MasterclassEnquiryCreateView

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'car-images', CarImageViewSet)
router.register(r'enquiries', EnquiryViewSet)
router.register(r'car-enquiries', CarEnquiryViewSet)
router.register(r'masterclass-enquiry', MasterclassEnquiryCreateView)

urlpatterns = router.urls
