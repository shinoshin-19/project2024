from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone

# Create your models here.

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        max_length = 10,
        blank = False,
        null = False,
    )

    email = models.EmailField(_('email address'), unique=True,
    blank = True,
    null = True,)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


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
    

