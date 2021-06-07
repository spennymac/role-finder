from django.contrib import admin

# Register your models here.
from roles.models import Role, Permission, RolePermission


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'cloud_provider']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission']
