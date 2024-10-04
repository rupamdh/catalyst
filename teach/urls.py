from django.urls import path
from .views import *


urlpatterns = [
    path('courses/', course_listing, name='courses'),
    path('courses/<str:slug>/', course_details, name='course_details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('course/add/', course_add, name='course_add'),
    path('course/edit/<str:slug>/', course_edit, name='course_edit'),

    path('my-courses/', my_courses, name='my_courses'),
    path('learn/<str:slug>/', learn, name='learn'),
]