from django.shortcuts import render
from lessons.models import Course, Classroom
from accounts.models import CustomUser
from datetime import time, timedelta, datetime
import random
# Sistemsel gün kısaltmaları
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

# Türkçe gün karşılıkları (template için)
day_names = {
    'Mon': 'Pazartesi',
    'Tue': 'Salı',
    'Wed': 'Çarşamba',
    'Thu': 'Perşembe',
    'Fri': 'Cuma'
}

# Saat blokları
START_HOURS = [9, 11, 13, 15, 17]  # 2 saatlik bloklar

# Tablo gösterimi için 50 dakikalık zaman aralıkları
time_slots = [
    "08:00-08:50", "09:00-09:50", "10:00-10:50",
    "11:00-11:50", "12:00-12:50", "13:00-13:50",
    "14:00-14:50", "15:00-15:50", "16:00-16:50",
    "17:00-17:50"  # Bunu EKLE!
]

def generate_schedule(request):
    all_courses = list(Course.objects.all()[:28])  # 4 sınıf * 7 ders
    instructors = list(CustomUser.objects.filter(role__title__in=["Öğretim Görevlisi", "Bölüm Başkanı"])[:10])
    classrooms = list(Classroom.objects.all())

    if len(all_courses) < 28 or len(instructors) < 10 or len(classrooms) < 7:
        return render(request, "schedule.html", {"error": "Yeterli sayıda ders, hoca veya sınıf yok."})

    schedule = []
    used_slots = set()
    course_idx = 0
    class_numbers = [1, 2, 3, 4]

    for sinif_index, sinif_no in enumerate(class_numbers):
        for i in range(7):  # Her sınıfa 7 ders
            course = all_courses[course_idx]
            instructor = instructors[course_idx % len(instructors)]
            classroom = classrooms[(course_idx + sinif_index) % len(classrooms)]

            slot_found = False
            for day in random.sample(DAYS, len(DAYS)):
                for hour in START_HOURS:
                    if (day, hour, instructor.id) in used_slots: continue
                    if (day, hour, classroom.id) in used_slots: continue
                    if (day, hour, sinif_index) in used_slots: continue

                    start_time = datetime.strptime(f"{hour}:00", "%H:%M")
                    slot_end = start_time + timedelta(minutes=50)
                    slot = f"{start_time.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"

                    schedule.append({
                        'sinif': sinif_no,  # <-- Türkçe 'ı' yerine düz 'i' kullandık!
                        'day': day,
                        'slot': slot,
                        'course': course.course_name,
                        'instructor': instructor.get_full_name(),
                        'classroom': classroom.classroom_name,
                    })

                    used_slots.add((day, hour, instructor.id))
                    used_slots.add((day, hour, classroom.id))
                    used_slots.add((day, hour, sinif_index))

                    slot_found = True
                    break
                if slot_found:
                    break

            course_idx += 1
    print("---------------schedule")
    print(schedule)
    print("---------------time_slots")
    print(time_slots)
    print("---------------class_numbers")
    print(class_numbers)
    print("---------------day_names")
    print(day_names)
    schedule_table = {}
    for day in DAYS:
        schedule_table[day] = {}
        for slot in time_slots:
            schedule_table[day][slot] = {s: None for s in class_numbers}

    # Mevcut schedule içindeki dersleri tabloya yerleştir
    for item in schedule:
        day = item['day']
        slot = item['slot']
        sinif = item['sinif']
        schedule_table[day][slot][sinif] = item
    

    return render(request, "schedule.html", {
        "schedule_table": schedule_table,
        "schedule": schedule,
        "time_slots": time_slots,
        "class_names": class_numbers,  # Sayısal sınıf listesi
        "day_names": day_names
    })