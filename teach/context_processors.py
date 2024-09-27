from .models import *

def teach_data(request):
    courses = Course.objects.all()
    total_course = courses.count()
    my_course = courses.filter(user=request.user) if request.user.is_authenticated else None
    my_course_count = my_course.count() if my_course else 0

    return {
        'courses' : courses,
        'total_course' : total_course,
        'my_course_count' : my_course_count
    }