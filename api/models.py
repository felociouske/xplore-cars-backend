from django.db import models
from cloudinary.models import CloudinaryField

class BaseCarFields(models.Model):
    ENGINE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    GRADE_CHOICES = [
        ('6', '6'),
        ('5', '5'),
        ('4.5', '4.5'),
        ('4', '4'),
        ('3.5', '3.5'),
        ('3', '3'),
        ('R', 'R'),
    ]

    name = models.CharField(max_length=100)
    make = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True, null=True)
    engine_type = models.CharField(max_length=10, choices=ENGINE_CHOICES, blank=True, null=True)
    mileage = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True 

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class BaseEnquiryFields(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True 

    def __str__(self):
        return f"Enquiry from {self.full_name}"


class Car(BaseCarFields):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('new', 'New'),
    ]
    transmission = models.CharField(max_length=50)
    features = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.name} - {self.make} {self.model} ({self.year})"

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Image"
        verbose_name_plural = "Car Images"

    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"

class Enquiry(BaseEnquiryFields):

    class Meta:
        verbose_name = "General Enquiry"
        verbose_name_plural = "General Enquiries"

    def __str__(self):
        return f"Enquiry from {self.full_name} - {self.subject or 'No Subject'}"


class CarEnquiry(models.Model):
    BUDGET_CHOICES = [
        ('below_1m', 'Below Ksh 1M'),
        ('1m_2m', 'Ksh 1M - 2M'),
        ('2m_3m', 'Ksh 2M - 3M'),
        ('above_3m', 'Above Ksh 3M'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, default="Inquiry about car import")
    vehicle_of_interest = models.CharField(max_length=100)
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, default="below_1m")
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Enquiry"
        verbose_name_plural = "Car Enquiries"

    def __str__(self):
        return f"Car Enquiry from {self.full_name} about {self.vehicle_of_interest}"

class MasterclassEnquiry(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Masterclass Enquiry"
        verbose_name_plural = "Masterclass Enquiries"

    def __str__(self):
        return f"Masterclass Enquiry - {self.full_name}"