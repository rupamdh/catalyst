from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from .utils import create_pagination
from .forms import CourseAddForm, LessonAddForm
from account.forms import ProfileImageChangeForm
from django.templatetags.static import static
import cv2
import datetime

# Create your views here.

def course_listing(request):
    courses = Course.objects.all().order_by('id')
    page_number = request.GET.get('page')
    page_courses = create_pagination(courses, page_number, 3)
    total_course = courses.count()
    start = 1
    end = 3




    context = {
        'page_courses' : page_courses,
        'total_course' : total_course,
        'start' : start,
        'end' : end
    }
    return render(request, 'teach/course_listing.html', context)

#view for course details page
def course_details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    is_in_cart = course.is_in_cart(request)
    is_in_order = course.is_in_order(request)


    context = {
        'course' : course,
        'is_in_cart' : is_in_cart,
        'is_in_order' : is_in_order
    }
    return render(request, 'teach/course_details.html', context)

#View for user dashboard
@login_required
def dashboard(request):
    if request.method == 'POST':
        pro_img_form = ProfileImageChangeForm(request.POST, request.FILES, instance=request.user)
        if pro_img_form.is_valid():
            pro_img_form.save()
            return redirect('dashboard')
            
    else:
        pro_img_form = ProfileImageChangeForm(instance=request.user)

    context ={
        'pro_img_form' : pro_img_form
    }
    return render(request, 'teach/dashboard.html', context)

#View for add course
@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseAddForm(request.POST, request.FILES)
        if form.is_valid():
            print('No error')
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('dashboard')
        else:
            print('error')
    else:
        form = CourseAddForm()
    return render(request, 'teach/course_add.html', {'form' : form})

#View for edit course
@login_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseAddForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('my_courses')
        lesson_form = LessonAddForm(request.POST)

    else:
        form = CourseAddForm(instance=course)
        lesson_form = LessonAddForm()
    context = {
        'course' : course,
        'form' : form,
        'lesson_form' : lesson_form
    }
    return render(request, 'teach/course_edit.html', context)

#View for show own added courses
@login_required
def my_courses(request):
    my_courses = Course.objects.filter(user=request.user)

    context = {
        'my_courses' : my_courses
    }
    return render(request, 'teach/my_courses.html', context)


@login_required
def learn(request, slug):
    course = get_object_or_404(Course, slug=slug)

    context = {
        'course' : course
    }
    return render(request, 'teach/learn.html', context)