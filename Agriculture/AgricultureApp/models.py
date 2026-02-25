from django.db import models
from django.utils import timezone
import hashlib


class UserProfile(models.Model):
    """User model for Farmers, Consumers, and Admins."""

    USER_TYPES = (
        ('Admin', 'Admin'),
        ('Farmer', 'Farmer'),
        ('Consumer', 'Consumer'),
    )

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    contact = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_active = models.BooleanField(default=True)
    blockchain_hash = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Product(models.Model):
    """Agricultural product with traceability information."""

    CATEGORY_CHOICES = (
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Grains', 'Grains'),
        ('Dairy', 'Dairy'),
        ('Other', 'Other'),
    )

    farmer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='products', limit_choices_to={'user_type': 'Farmer'}
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Other')
    image = models.ImageField(upload_to='products/', blank=True)
    origin_location = models.CharField(max_length=300, blank=True)
    harvest_date = models.DateField(null=True, blank=True)
    blockchain_hash = models.CharField(max_length=255, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} by {self.farmer.username}"

    @property
    def trace_id(self):
        """Generate unique trace ID for QR code."""
        raw = f"{self.farmer.username}-{self.name}-{self.pk}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


class TransportLog(models.Model):
    """Transport/supply chain log for product traceability."""

    STAGE_CHOICES = (
        ('Harvested', 'Harvested'),
        ('Packed', 'Packed'),
        ('InTransit', 'In Transit'),
        ('AtWarehouse', 'At Warehouse'),
        ('Delivered', 'Delivered'),
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='transport_logs'
    )
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    location = models.CharField(max_length=300)
    handler = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.product.name} — {self.stage} at {self.location}"


class Purchase(models.Model):
    """Purchase record linking consumer to product."""

    consumer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='purchases', limit_choices_to={'user_type': 'Consumer'}
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    farmer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='sales', limit_choices_to={'user_type': 'Farmer'}
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    blockchain_hash = models.CharField(max_length=255, blank=True)
    purchased_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-purchased_at']

    def __str__(self):
        return f"{self.consumer.username} bought {self.product.name}"
