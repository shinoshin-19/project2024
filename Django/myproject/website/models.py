from django.db import models
from django.urls import reverse_lazy

# Create your models here.

class Creater(models.Model):
    name = models.CharField(
        max_length = 10,
        blank = False,
        null = False,
    )

    def __str__(self):
        return self.name
    

class Status(models.Model):
    name = models.CharField(
        max_length = 10,
        blank = False,
        null = False,
    )

    def __str__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(
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
        on_delete = models.CASCADE
    )

    creater = models.ForeignKey(
        Creater,
        on_delete = models.CASCADE
    )
 

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(
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
        on_delete = models.CASCADE
    )

    status = models.ForeignKey(
        Status,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # /detail/1/
        return reverse_lazy("detail", args=[self.id])
    

