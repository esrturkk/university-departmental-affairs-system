from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from .models import CustomUser, Student, Role

# Register your models here.

class CustomUserAdmin(ImportExportMixin, UserAdmin):
    model = CustomUser
    list_display = [
        'username',
        'first_name',
        'last_name',
        'role',
        'email',
    ]
    fieldsets = UserAdmin.fieldsets + (('Görev bilgisi', {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Kişisel bilgiler', {'fields': ('first_name', 'last_name', 'email')}), ('Görev bilgisi', {'fields': ('role',)}),)

class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_no',
        'first_name',
        'last_name',
        'email',
        ]
    fieldsets = ((None, {'fields': ('student_no',)}), ('Kişisel bilgiler', {'fields': ('first_name', 'last_name', 'email',)}),)

class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'type',
        ]
    fieldsets = ((None, {'fields': ('id', 'title', 'type',)}),)
    readonly_fields = ('id',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Role, RoleAdmin)
