from django.db import models
from account.models import User
from django.core.exceptions import ValidationError
from core.utils import create_unique_slug
from datetime import datetime
from django.utils import timezone 
import os

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=400, unique=True, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(self.title, Category)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'

def rename_image(instance, filename):
    upload_to = 'course/thumb/'
    ext = filename.split('.')[-1]
    last_course_id = Course.objects.filter().last().id
    filename = '{}.{}'.format(f'thumb-{int(last_course_id+1)}', ext)
    return os.path.join(upload_to, filename)

class Course(models.Model):
    LEVEL_CHOICE = (
        ('B', 'Begainer'),
        ('I', 'Intermediate'),
        ('A', 'Advance'),
        ('E', 'Expert'),
    )

    DEFAULT = 'static/images/placeholder.png'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=400, unique=True, null=True, blank=True, editable=False)
    short_desc = models.CharField(max_length=600, help_text='Course description should be less than 600 charecter.')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Choose Categories')
    price = models.PositiveIntegerField(default=0, verbose_name='Regular Price')
    off_price = models.PositiveIntegerField(default=None, verbose_name='Discounted Price', null=True, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICE, default=None, null=True, blank=True, verbose_name='Difficulty Level')
    thumbnail = models.ImageField(upload_to=rename_image)
    preview_video = models.FileField(upload_to='course/video/', null=True)
    

    def clean(self):
        #Validation for price
        if self.price and self.off_price:
            if self.off_price > self.price:
                raise ValidationError("Offer price can't bigger than original price")
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(self.title, Course)
        self.clean()
        return super().save(*args, **kwargs)
    
    def get_price(self):
        return self.off_price if self.off_price else self.price
    
    def is_in_cart(self, request):
        from shop.models import Cart
        cart = Cart.objects.filter(user=request.user, course=self).exists()
        return cart
    
    def __str__(self):
        return self.title
    