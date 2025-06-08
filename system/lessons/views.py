from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from accounts.models import CustomUser
from .models import Course, Classroom, CourseSchedule
from .forms import CourseForm, ClassroomForm
from accounts.views import AuthorizationRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from functools import wraps
import random
from datetime import time
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

class CourseListView(AuthorizationRequiredMixin, ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses'

class CourseCreateView(AuthorizationRequiredMixin, CreateView):
    model = Course
    template_name = 'course_new.html'
    context_object_name = 'course'
    form_class = CourseForm
    
    def get_success_url(self):
        return reverse_lazy('courses')

class CourseUpdateView(AuthorizationRequiredMixin, UpdateView):
    model = Course
    template_name = 'course_edit.html'
    context_object_name = 'course'
    form_class = CourseForm

    def get_success_url(self):
        return reverse_lazy('courses')

class CourseDeleteView(AuthorizationRequiredMixin, DeleteView):
    model = Course
    template_name = 'course_delete.html'
    context_object_name = 'course'
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

MIN_COURSES = 10
MIN_INSTRUCTORS = 5
MIN_CLASSROOMS = 3

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
def course_schedule_generate(request):
    if request.method == 'POST':
        CourseSchedule.objects.all().delete()

        courses = list(Course.objects.all())
        instructors = list(CustomUser.objects.filter(role__title__in=['Öğretim Elemanı', 'Bölüm Başkanı']))
        classrooms = list(Classroom.objects.all())

        if len(courses) < MIN_COURSES or len(instructors) < MIN_INSTRUCTORS or len(classrooms) < MIN_CLASSROOMS:
            return render(request, 'course_schedule_generate.html', {'error': 'Yeterli sayıda ders, öğretim elemanı veya derslik bulunamadı.'})

        instructor_schedule = {inst.id: [] for inst in instructors}
        classroom_schedule = {room.id: [] for room in classrooms}

        daily_slots = []
        for day in DAYS:
            for start_hour in START_HOURS:
                start = time(start_hour, 0)
                end = (datetime.combine(datetime.today(), start) + timedelta(minutes=50)).time()
                daily_slots.append((day, start, end))

        def is_conflict(schedule_list, day, start, end):
            for d, s, e in schedule_list:
                if d == day:
                    if not (end <= s or start >= e):
                        return True
            return False

        for course in courses:
            instructor = course.course_instructor
            if not instructor:
                continue

            assigned = False
            random.shuffle(daily_slots)
            random.shuffle(classrooms)

            for day, start, end in daily_slots:
                if is_conflict(instructor_schedule[instructor.id], day, start, end):
                    continue

                suitable_classroom = None
                for room in classrooms:
                    if not is_conflict(classroom_schedule[room.id], day, start, end):
                        suitable_classroom = room
                        break

                if suitable_classroom is None:
                    continue

                CourseSchedule.objects.create(
                    course=course,
                    classroom=suitable_classroom,
                    day_of_week=day,
                    start_time=start,
                    end_time=end,
                )

                instructor_schedule[instructor.id].append((day, start, end))
                classroom_schedule[suitable_classroom.id].append((day, start, end))

                assigned = True
                break

            if not assigned:
                return render(request, 'course_schedule_generate.html', {
                    'error': f'Ders "{course.course_name}" için uygun saat ve derslik bulunamadı.'
                })

        return redirect('course_schedule_generate')

    schedules = CourseSchedule.objects.all()

    schedule = []
    for sc in schedules:
        schedule.append({
            'class': sc.course.course_level,
            'day': sc.day_of_week,
            'slot': f'{sc.start_time.strftime('%H:%M')}-{sc.end_time.strftime('%H:%M')}',
            'course': sc.course.course_name,
            'instructor': sc.course.course_instructor.get_full_name() if sc.course.course_instructor else 'N/A',
            'classroom': sc.classroom.classroom_name if sc.classroom else 'N/A',
        })

    schedule_table = {}
    class_levels = sorted(set(item['class'] for item in schedule))

    for day in DAYS:
        schedule_table[day] = {}
        for slot in time_slots:
            schedule_table[day][slot] = {level: None for level in class_levels}

    for item in schedule:
        day = item['day']
        slot = item['slot']
        class_no = item['class']
        schedule_table[day][slot][class_no] = item

    return render(request, 'course_schedule_generate.html', {
        'schedule_table': schedule_table,
        'schedule': schedule,
        'time_slots': time_slots,
        'class_names': class_levels,
        'day_names': day_names
    })

@login_required(login_url='home')
def course_schedule_view(request, user_id=None):
    viewer = request.user
    
    if user_id is None:
        selected_user = viewer
    else:
        try:
            selected_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return HttpResponse('Kullanıcı bulunamadı.', status=404)

    schedules = CourseSchedule.objects.filter(course__course_instructor=selected_user)

    schedule = []
    for sc in schedules:
        schedule.append({
            'class': sc.course.course_level,
            'day': sc.day_of_week,
            'slot': f'{sc.start_time.strftime("%H:%M")}-{sc.end_time.strftime("%H:%M")}',
            'course': sc.course.course_name,
            'instructor': sc.course.course_instructor.get_full_name() if sc.course.course_instructor else 'N/A',
            'classroom': sc.classroom.classroom_name if sc.classroom else 'N/A',
        })

    schedule_table = {}
    class_levels = sorted(set(item['class'] for item in schedule))

    for day in DAYS:
        schedule_table[day] = {}
        for slot in time_slots:
            schedule_table[day][slot] = {level: None for level in class_levels}

    for item in schedule:
        day = item['day']
        slot = item['slot']
        class_no = item['class']
        schedule_table[day][slot][class_no] = item

    context = {
        'schedule_table': schedule_table,
        'time_slots': time_slots,
        'class_names': class_levels,
        'day_names': day_names,
        'user': viewer,
        'selected_user': selected_user,
    }

    if request.method == 'POST':
        template = get_template('course_schedule_pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ders_programi.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('PDF oluşturulurken hata oluştu.')
        return response

    return render(request, 'course_schedule_view.html', context)

class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = 'classrooms.html'
    context_object_name = 'classrooms'

class ClassroomDetailView(LoginRequiredMixin, DetailView):
    model = Classroom
    template_name = 'classroom_detail.html'
    context_object_name = 'classroom'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = self.get_object()
        context['classroom_lessons'] = CourseSchedule.objects.filter(classroom=classroom).order_by('day_of_week', 'start_time')
        return context

class ClassroomCreateView(AuthorizationRequiredMixin, CreateView):
    model = Classroom
    template_name = 'classroom_new.html'
    context_object_name = 'classroom'
    form_class = ClassroomForm
    
    def get_success_url(self):
        return reverse_lazy('classrooms')

class ClassroomUpdateView(AuthorizationRequiredMixin, UpdateView):
    model = Classroom
    template_name = 'classroom_edit.html'
    context_object_name = 'classroom'
    form_class = ClassroomForm

    def get_success_url(self):
        return reverse_lazy('classrooms')

class ClassroomDeleteView(AuthorizationRequiredMixin, DeleteView):
    model = Classroom
    template_name = 'classroom_delete.html'
    context_object_name = 'classroom'
    success_url = reverse_lazy('classrooms')
