from django.db import models
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from urllib.parse import urlparse, parse_qs


class Car(models.Model):
    GRADE_CHOICES = [
        ('6', '6'),
        ('5', '5'),
        ('4.5', '4.5'),
        ('4', '4'),
        ('3.5', '3.5'),
        ('3', '3'),
        ('R', 'R'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('new', 'New'),
    ]
    BODY_TYPE_CHOICES = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('crossover', 'Crossover'),
        ('wagon', 'Wagon'),
        ('minivan', 'Minivan'),
        ('pickup', 'Pickup'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('van', 'Van'),
    ]
    IMPORT_TYPE_CHOICES = [
        ('japan_import', 'Japan Import'),
        ('local', 'Local'),
    ]
    DRIVE_CHOICES = [
        ('rhd', 'Right Hand Drive'),
        ('lhd', 'Left Hand Drive'),
    ]

    CATEGORY_CHOICES = [
        ('available_to_import', 'Available to Import'),
        ('successful_import', 'Successful Import'),
        ('popular_in_kenya', 'Popular in Kenya'),
    ]

    # Price range
    price_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_to = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Core identity
    make = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Toyota, Nissan, Mazda")
    model = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Prado, Note, Demio")
    year = models.PositiveIntegerField(blank=True, null=True, help_text="e.g. 2019")
    name = models.CharField(max_length=100, blank=True, null=True, help_text="Auto-filled if left blank")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='available_to_import')

    youtube_video_1 = models.URLField(max_length=500, blank=True, null=True,
        help_text="YouTube video URL e.g. https://www.youtube.com/watch?v=xxxx")
    youtube_video_1_title = models.CharField(max_length=200, blank=True, null=True,
        help_text="e.g. Review after arrival")

    youtube_video_2 = models.URLField(max_length=500, blank=True, null=True,
        help_text="Second YouTube video URL (optional)")
    youtube_video_2_title = models.CharField(max_length=200, blank=True, null=True,
        help_text="e.g. Receiving the car")

    youtube_video_3 = models.URLField(max_length=500, blank=True, null=True,
        help_text="Third YouTube video URL (optional)")
    youtube_video_3_title = models.CharField(max_length=200, blank=True, null=True,
        help_text="e.g. Full walkaround")

    youtube_video_4 = models.URLField(max_length=500, blank=True, null=True,
        help_text="Fourth YouTube video URL (optional)")
    youtube_video_4_title = models.CharField(max_length=200, blank=True, null=True,
        help_text="e.g. Customer testimonial")

    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True, null=True)
    import_type = models.CharField(max_length=20, choices=IMPORT_TYPE_CHOICES, default='japan_import')
    trim_levels = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Comma-separated trim levels e.g. X, G, Moda, TRD Sportivo"
    )
    features = models.TextField(blank=True, null=True)
    description = CKEditor5Field(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.name and (self.make or self.model):
            parts = [p for p in [self.make, self.model, str(self.year) if self.year else None] if p]
            self.name = " ".join(parts)
        super().save(*args, **kwargs)

    def price_display(self):
        """Returns formatted price range string e.g. KES 954,000 - 1,500,000"""
        if not self.price_from:
            return ""
        base = f"KES {int(self.price_from):,}"
        if self.price_to:
            return f"{base} - {int(self.price_to):,}"
        return base


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Image"
        verbose_name_plural = "Car Images"

    def __str__(self):
        return f"Image for {self.car.name or f'Car #{self.car.id}'}"


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
    vehicle_of_interest = models.CharField(max_length=100)
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='below_1m')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Enquiry"
        verbose_name_plural = "Car Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Car Enquiry from {self.full_name} about {self.vehicle_of_interest}"


class ContactEnquiry(models.Model):
    SUBJECT_TYPE_CHOICES = [
        ('general', 'General'),
        ('masterclass', 'Masterclass'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE_CHOICES, default='general')
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Enquiry"
        verbose_name_plural = "Contact Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_subject_type_display()} enquiry from {self.full_name}"


class Testimonial(models.Model):
    DISPLAY_CHOICES = [
        ('text', 'Text Only'),
        ('video', 'Video Only'),
        ('both', 'Text + Video'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author_name = models.CharField(max_length=150, blank=True, null=True)
    author_role = models.CharField(max_length=150, blank=True, null=True)
    testimonial_text = models.TextField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    youtube_id = models.CharField(max_length=50, blank=True, null=True, editable=False)
    layout_type = models.CharField(max_length=10, choices=DISPLAY_CHOICES, default='text')
    rating = models.PositiveSmallIntegerField(default=5)
    featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.title} - {self.author_name or 'Anonymous'}"

    def extract_youtube_id(self):
        if not self.youtube_url:
            return None
        parsed = urlparse(self.youtube_url)
        if 'youtube' in parsed.netloc:
            return parse_qs(parsed.query).get('v', [None])[0]
        elif 'youtu.be' in parsed.netloc:
            return parsed.path.strip('/')
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "testimonial"
            slug_candidate = base_slug
            counter = 1
            while Testimonial.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate

        if self.youtube_url:
            self.youtube_id = self.extract_youtube_id()

        super().save(*args, **kwargs)

    def youtube_embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}" if self.youtube_id else None


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    cover_image = CloudinaryField('image', blank=True, null=True)
    content = CKEditor5Field()
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts',
    )
    youtube_url = models.URLField(blank=True, null=True, help_text="Optional: link a YouTube video to this post")
    youtube_id = models.CharField(max_length=50, blank=True, null=True, editable=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def extract_youtube_id(self):
        if not self.youtube_url:
            return None
        parsed = urlparse(self.youtube_url)
        if 'youtube' in parsed.netloc:
            return parse_qs(parsed.query).get('v', [None])[0]
        elif 'youtu.be' in parsed.netloc:
            return parsed.path.strip('/')
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            slug_candidate = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate

        if self.youtube_url:
            self.youtube_id = self.extract_youtube_id()

        super().save(*args, **kwargs)

    def youtube_embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}" if self.youtube_id else None
