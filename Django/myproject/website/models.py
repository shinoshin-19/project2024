from django.db import models
from django.urls import reverse_lazy

# Create your models here.

class User(models.Model):
    name = models.CharField(
        max_length = 10,
        blank = False,
        null = False,
    )

    def __str__(self):
        return self.name
    

class Status(models.Model):
    title = models.CharField(
        max_length = 10,
        blank = False,
        null = False,
    )


class Priority(models.Model):
    title = models.CharField(
        max_length = 10,
        blank = False,
        null = False,
    )

    priority = models.IntegerField(
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.title
    
class Project(models.Model):
    title = models.CharField(
        max_length = 30,
        blank = False,
        null = False,
    )

    deadline = models.DateField(
        editable = True,
        blank = False,
        null = False
    )

    note = models.TextField(
        blank = True,
        null = True

    )

    created = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        blank = False,
        null = False,
    )

    updated = models.DateTimeField(
        auto_now = True,
        editable = False,
        blank = False,
        null = False,
    )

    status = models.ForeignKey(
        Status,
        on_delete = models.CASCADE,
        blank = True,
        null = True,
    )

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )
 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # /detail/1/
        return reverse_lazy("detailproject", args=[self.id])


class Task(models.Model):
    title = models.CharField(
        max_length = 30,
        blank = False,
        null = False,
    )

    deadline = models.DateField(
        editable = True,
        blank = False,
        null = False
    )

    note = models.TextField(
        blank = True,
        null = True

    )

    workload = models.IntegerField(
        blank = True,
        null = True,
    )

    created = models.DateTimeField(
        auto_now_add = True,
        editable = False,
        blank = False,
        null = False,
    )

    updated = models.DateTimeField(
        auto_now = True,
        editable = False,
        blank = False,
        null = False,
    )

    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )

    status = models.ForeignKey(
        Status,
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )

    priority = models.ForeignKey(
        Priority,
        on_delete = models.CASCADE,
        blank = True,
        null = True

    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # /detail/1/
        return reverse_lazy("detailtask", args=[self.id])
    

