from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from django import forms
from .models import Task, Project


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
        )

# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "deadline", "note", "status", "project", "workload", "priority"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        # super()を削除
        # super(TaskForm, self).__init__(*args, **kwargs)
        # 以下にフォームの初期化コードを書く
        super().__init__(*args, **kwargs)
        
        # スーパーユーザーの場合はすべてのプロジェクトを表示し、一般ユーザーの場合はログインユーザーに関連するプロジェクトのみを表示
        if user.is_superuser:
            self.fields['project'].queryset = Project.objects.all()
        else:
            self.fields['project'].queryset = Project.objects.filter(user_id=user.id)