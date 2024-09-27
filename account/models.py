from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import os

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have a email.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
def rename_user_image(instance, filename):
    upload_to = 'user/profile/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(f'user_{int(instance.pk)}', ext)
    
    return os.path.join(upload_to, filename)


class User(AbstractUser):
    ROLE_CHOICE = (
        ('E', 'Educator'),
        ('S', 'Student'),
    )
    username = None
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to=rename_user_image, null=True, blank=True)
    role = models.CharField(max_length=2, default='S', choices=ROLE_CHOICE)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def total_course(self):
        from teach.models import Course
        courses = Course.objects.filter(user=self)
        return courses.count()
    
    def cart_count(self):
        from shop.models import Cart
        carts = Cart.objects.filter(user=self)
        return carts.count()


    def __str__(self):
        return self.email


class EducatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role' : 'E'})
    bio = models.CharField(max_length=500, default='')
    facebook_url = models.URLField(verbose_name='Facebook profile URL', null=True, blank=True)
    twitter_url = models.URLField(verbose_name='Twitter profile URL', null=True, blank=True)
    linkedin_url = models.URLField(verbose_name='LinkedIn profile URL', null=True, blank=True)
    instagram_url = models.URLField(verbose_name='Instagram profile URL', null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        verbose_name_plural = 'Educator Profiles'