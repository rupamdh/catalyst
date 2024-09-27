from django.db import models
from teach.models import Course
from account.models import User

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_course')

    class Meta:
        unique_together = ('user', 'course', )
    
    def __str__(self):
        return f'{self.user} - {self.course}'

class Order(models.Model):
    STATUS_CHOICE = (
        ('CM', 'Completed'),
        ('PD', 'Pending'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_course')
    status = models.CharField(max_length=2, choices=STATUS_CHOICE)
    

    class Meta:
        unique_together = ('user', 'course', )
    
    def __str__(self):
        return f'{self.user} - {self.course}'