from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Extended user model for the e-commerce shop.
    Inherits: username, email, password, first_name, last_name,
              is_staff, is_active, date_joined from AbstractUser.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone  = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True
    )
    address      = models.CharField(max_length=255, blank=True)
    city         = models.CharField(max_length=100, blank=True)
    postal_code  = models.CharField(max_length=20,  blank=True)
    country      = models.CharField(max_length=100, blank=True)
    # Track newsletter opt-in
    newsletter   = models.BooleanField(default=False)
    # Timestamps
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    USERNAME_FIELD  = 'email'     # log in with email instead of username
    REQUIRED_FIELDS = ['username'] # still required for createsuperuser
    class Meta:
        verbose_name        = _('user')
        verbose_name_plural = _('users')
        ordering            = ['-date_joined']
    def __str__(self):
        return self.email
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email
    @property
    def has_complete_profile(self):
        """Check if user has filled in shipping address fields."""
        return all([self.address, self.city, self.postal_code, self.country])

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
    ]
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

SUBJECT_CHOICES = [
    ('order',   'Order & Shipping'),
    ('return',  'Returns & Refunds'),
    ('product', 'Product Question'),
    ('account', 'Account & Payments'),
    ('other',   'Other'),
]


class ContactMessage(models.Model):
    name        = models.CharField(max_length=100)
    email       = models.EmailField()
    subject     = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    is_read     = models.BooleanField(default=False)

    # Reply fields
    reply       = models.TextField(blank=True, default='')
    replied_at  = models.DateTimeField(null=True, blank=True)
    replied_by  = models.ForeignKey(
        'CustomUser',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='contact_replies',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name        = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"[{self.get_subject_display()}] {self.name} <{self.email}>"

    @property
    def is_replied(self):
        return bool(self.replied_at)