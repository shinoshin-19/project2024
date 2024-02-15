from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass