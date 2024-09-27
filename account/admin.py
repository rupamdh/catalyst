from django.contrib import admin
from .models import User, EducatorProfile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role')

admin.site.register(User, UserAdmin)


admin.site.register(EducatorProfile)