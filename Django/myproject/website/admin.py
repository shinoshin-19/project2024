from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

# Register your models here.

admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Priority)
class PriorityAdmin(admin.ModelAdmin):
    pass