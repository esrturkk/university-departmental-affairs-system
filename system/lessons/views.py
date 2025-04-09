from django.shortcuts import render
from accounts.models import CustomUser
from lessons.models import Course, Classroom
from datetime import time, timedelta, datetime
import random

# System day abbreviations
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

# Turkish day names for templates
day_names = {
    'Mon': 'Pazartesi',
    'Tue': 'Salı',
    'Wed': 'Çarşamba',
    'Thu': 'Perşembe',
    'Fri': 'Cuma'
}

# Start hours for 2-hour blocks
START_HOURS = [9, 11, 13, 15, 17]

# 50-minute time slots for table display
time_slots = [
    '08:00-08:50', '09:00-09:50', '10:00-10:50',
    '11:00-11:50', '12:00-12:50', '13:00-13:50',
    '14:00-14:50', '15:00-15:50', '16:00-16:50',
    '17:00-17:50'
]

# 50-minute time slots for table display
time_slots = [
    '08:00-08:50', '09:00-09:50', '10:00-10:50',
    '11:00-11:50', '12:00-12:50', '13:00-13:50',
    '14:00-14:50', '15:00-15:50', '16:00-16:50',
    '17:00-17:50'
]

def generate_schedule(request):
    all_courses = list(Course.objects.all()[:28])  # 4 classes * 7 courses
    instructors = list(CustomUser.objects.filter(role__title__in=['Öğretim Görevlisi', 'Bölüm Başkanı'])[:10])
    classrooms = list(Classroom.objects.all())

    if len(all_courses) < 28 or len(instructors) < 10 or len(classrooms) < 7:
        return render(request, 'schedule.html', {'error': 'Yeterli sayıda ders, öğretim elemanı veya sınıf bulunamadı.'})

    schedule = []
    used_slots = set()
    course_idx = 0
    class_numbers = [1, 2, 3, 4]

    for class_index, class_no in enumerate(class_numbers):
        for i in range(7):  # 7 courses per class
            course = all_courses[course_idx]
            instructor = instructors[course_idx % len(instructors)]
            classroom = classrooms[(course_idx + class_index) % len(classrooms)]

            slot_found = False
            for day in random.sample(DAYS, len(DAYS)):
                for hour in START_HOURS:
                    if (day, hour, instructor.id) in used_slots: continue
                    if (day, hour, classroom.id) in used_slots: continue
                    if (day, hour, class_index) in used_slots: continue

                    start_time = datetime.strptime(f'{hour}:00', '%H:%M')
                    slot_end = start_time + timedelta(minutes=50)
                    slot = f'{start_time.strftime("%H:%M")}-{slot_end.strftime("%H:%M")}'

                    schedule.append({
                        'class': class_no,
                        'day': day,
                        'slot': slot,
                        'course': course.course_name,
                        'instructor': instructor.get_full_name(),
                        'classroom': classroom.classroom_name,
                    })

                    used_slots.add((day, hour, instructor.id))
                    used_slots.add((day, hour, classroom.id))
                    used_slots.add((day, hour, class_index))

                    slot_found = True
                    break
                if slot_found:
                    break

            course_idx += 1

    schedule_table = {}
    for day in DAYS:
        schedule_table[day] = {}
        for slot in time_slots:
            schedule_table[day][slot] = {c: None for c in class_numbers}

    for item in schedule:
        day = item['day']
        slot = item['slot']
        class_no = item['class']
        schedule_table[day][slot][class_no] = item

    return render(request, 'schedule.html', {
        'schedule_table': schedule_table,
        'schedule': schedule,
        'time_slots': time_slots,
        'class_names': class_numbers,
        'day_names': day_names
    })