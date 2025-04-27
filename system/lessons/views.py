from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from accounts.models import CustomUser
from .models import Course, Classroom, CourseSchedule
from .forms import CourseForm
from accounts.views import AuthorizationRequiredMixin
from datetime import timedelta, datetime
from functools import wraps
import random

class CourseListView(AuthorizationRequiredMixin, ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'

class CourseCreateView(AuthorizationRequiredMixin, CreateView):
    model = Course
    template_name = 'course_new.html'
    context_object_name = 'courses'
    form_class = CourseForm
    
    def get_success_url(self):
        return reverse_lazy('courses')

class CourseUpdateView(AuthorizationRequiredMixin, UpdateView):
    model = Course
    template_name = 'course_edit.html'
    context_object_name = 'courses'
    form_class = CourseForm

    def get_success_url(self):
        return reverse_lazy('courses')

class CourseDeleteView(AuthorizationRequiredMixin, DeleteView):
    model = Course
    template_name = 'course_delete.html'
    context_object_name = 'courses'
    success_url = reverse_lazy('courses')

DAYS = ['Pzt', 'Sal', 'Çrş', 'Prş', 'Cum']
day_names = {
    'Pzt': 'Pazartesi',
    'Sal': 'Salı',
    'Çrş': 'Çarşamba',
    'Prş': 'Perşembe',
    'Cum': 'Cuma'
}

START_HOURS = [9, 11, 13, 15, 17]
time_slots = [
    '08:00-08:50', '09:00-09:50', '10:00-10:50',
    '11:00-11:50', '12:00-12:50', '13:00-13:50',
    '14:00-14:50', '15:00-15:50', '16:00-16:50',
    '17:00-17:50'
]

MIN_COURSES = 28
MIN_INSTRUCTORS = 10
MIN_CLASSROOMS = 7

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated or not hasattr(user, 'role') or user.role.title not in allowed_roles:
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@role_required(['Bölüm Başkanı', 'Bölüm Sekreteri'])
def courseScheduleGenerator(request):
    if request.method == 'POST':
        CourseSchedule.objects.all().delete()

        courses = list(Course.objects.all())
        instructors = list(CustomUser.objects.filter(role__title__in=['Öğretim Elemanı', 'Bölüm Başkanı']))
        classrooms = list(Classroom.objects.all())

        if len(courses) < MIN_COURSES or len(instructors) < MIN_INSTRUCTORS or len(classrooms) < MIN_CLASSROOMS:
            return render(request, 'scheduleGenerator.html', {'error': 'Yeterli sayıda ders, öğretim elemanı veya derslik bulunamadı.'})

        used_slots = set()

        for course_idx, course in enumerate(courses):
            instructor = instructors[course_idx % len(instructors)]
            classroom = classrooms[course_idx % len(classrooms)]

            slot_found = False
            for day in random.sample(DAYS, len(DAYS)):
                for hour in START_HOURS:
                    if (day, hour, instructor.id) in used_slots: continue
                    if (day, hour, classroom.id) in used_slots: continue

                    start_time = datetime.strptime(f'{hour}:00', '%H:%M')
                    slot_end = start_time + timedelta(minutes=50)

                    CourseSchedule.objects.create(
                        course=course,
                        classroom=classroom,
                        instructor=instructor,
                        day_of_week=day,
                        start_time=start_time.time(),
                        end_time=slot_end.time(),
                    )

                    used_slots.add((day, hour, instructor.id))
                    used_slots.add((day, hour, classroom.id))

                    slot_found = True
                    break
                if slot_found:
                    break
    
        return redirect('courseScheduleGenerator')


    schedules = CourseSchedule.objects.all()

    schedule = []
    for sc in schedules:
        schedule.append({
            'class': sc.course.course_level,
            'day': sc.day_of_week,
            'slot': f'{sc.start_time.strftime('%H:%M')}-{sc.end_time.strftime('%H:%M')}',
            'course': sc.course.course_name,
            'instructor': sc.instructor.get_full_name() if sc.instructor else 'N/A',
            'classroom': sc.classroom.classroom_name if sc.classroom else 'N/A',
        })

    schedule_table = {}
    class_numbers = [1, 2, 3, 4]

    for day in DAYS:
        schedule_table[day] = {}
        for slot in time_slots:
            schedule_table[day][slot] = {c: None for c in class_numbers}

    for item in schedule:
        day = item['day']
        slot = item['slot']
        class_no = item['class']
        schedule_table[day][slot][class_no] = item

    return render(request, 'courseScheduleGenerator.html', {
        'schedule_table': schedule_table,
        'schedule': schedule,
        'time_slots': time_slots,
        'class_names': class_numbers,
        'day_names': day_names
    })

def courseScheduleViewer(request):
    pass