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
    payment_method = models.CharField(max_length=50, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    

    class Meta:
        unique_together = ('user', 'course', )
    
    def __str__(self):
        return f'{self.user} - {self.course}'
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='review_course')
    rating = models.FloatField()
    text = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course', )
    
    def __str__(self):
        return f'{self.user} - {self.course} - {self.rating}'
    
    