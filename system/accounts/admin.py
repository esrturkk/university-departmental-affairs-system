from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from .models import CustomUser, Role

# Register your models here.

class CustomUserAdmin(ImportExportMixin, UserAdmin):
    model = CustomUser
    list_display = [
        'username',
        'first_name',
        'last_name',
        'role',
        'email',
        'is_staff',
    ]

    fieldsets = UserAdmin.fieldsets + (('Görev bilgisi', {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Görev bilgisi', {'fields': ('role',)}),)

class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        ]
    fieldsets = (
        (None, {'fields': ('id', 'title',)}),)
    readonly_fields = ('id',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
