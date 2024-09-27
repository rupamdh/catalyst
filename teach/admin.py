from django.contrib import admin
from .models import Course, Category

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category')

admin.site.register(Course, CourseAdmin)

admin.site.register(Category)