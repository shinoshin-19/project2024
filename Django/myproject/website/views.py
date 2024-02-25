from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView 
from .models import *
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.db.models import Avg,Sum,Max,Min,Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from .forms import SignUpForm, LoginFrom # ログインフォームをimport
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm



"""
class TopIndex(LoginRequiredMixin,ListView):
    template_name = "website/index.html"
    login_url = '/login'#ログインしていないユーザーのリダイレクト先ログインページ
    model = Task

    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)

        tasks = Task.objects.all().order_by('-priority_id')
        # タスクごとの残り日数を計算してコンテキストに追加する
        # 今日の日付を抽出
        today = datetime.now().date()
        # 残り日数データを保存するリストを作成
        remaining_days_list = []
        # 各タスクの期限から今日の日付を引いて、残りに数を抽出
        for task in tasks:
             # deadlineがNullでない場合
            if task.deadline is not None:
                 remaining_days = (task.deadline - today).days

            else:
                remaining_days = "-"

            remaining_days_list.append(remaining_days)

        task_info_list = [{'task':task,'remaining_days':remaining_days} for task,remaining_days in zip(tasks,remaining_days_list)]

        context['task_info_list'] = task_info_list

        return context
""" 

class TopIndex(LoginRequiredMixin,ListView):
    template_name = "website/index.html"
    login_url = '/login'#ログインしていないユーザーのリダイレクト先ログインページ
    model = Task

    def get_queryset(self):
        if self.request.user.is_superuser:
            # スーパーユーザーはすべてのタスクを取得
            return Task.objects.all()
        else:
            # 一般ユーザーは自分のタスクのみを取得
            return Task.objects.filter(project__user=self.request.user)


    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)

        tasks = Task.objects.all().order_by('-priority_id')
        # タスクごとの残り日数を計算してコンテキストに追加する
        # 今日の日付を抽出
        today = datetime.now().date()
        # 残り日数データを保存するリストを作成
        remaining_days_list = []
        # 各タスクの期限から今日の日付を引いて、残りに数を抽出
        for task in tasks:
             # deadlineがNullでない場合
            if task.deadline is not None:
                 remaining_days = (task.deadline - today).days

            else:
                remaining_days = "-"

            remaining_days_list.append(remaining_days)

        task_info_list = [{'task':task,'remaining_days':remaining_days} for task,remaining_days in zip(tasks,remaining_days_list)]

        context['task_info_list'] = task_info_list

        return context




class Index(LoginRequiredMixin,ListView):
# 一覧するモデルを指定する -> 'object_list'で取得可能
    model = Task


# ListViewは、一覧を簡単に作るためのView
class UserIndex(LoginRequiredMixin,ListView):
    # 一覧するモデルを指定する -> 'object_list'で取得可能
    # template_name = "website/user_list.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_with_counts'] = User.objects.annotate(
            project_count=Count('project', distinct=True),
            task_count=Count('project__task', distinct=True)
        )
        return context
    



class ProjectIndex(LoginRequiredMixin,ListView):
    # 一覧するモデルを指定する -> 'object_list'で取得可能
    model = Project


    def get_queryset(self):
        if self.request.user.is_superuser:
            # スーパーユーザーはすべてのタスクを取得
            return Project.objects.all()
        else:
            # 一般ユーザーは自分のタスクのみを取得
            return Project.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # プロジェクトの一覧を取得
        projects = self.get_queryset()

        # プロジェクトごとの残り日数を計算してコンテキストに追加
        today = datetime.now().date()
        remaining_days_list = []
        for project in projects:
            if project.deadline is not None:        
                remaining_days = (project.deadline - today).days
            else:
                remaining_days = "-"  # deadlineがNullの場合、特定の記号を代入
            remaining_days_list.append(remaining_days)

        # プロジェクト情報と残り日数を組み合わせてリストに追加
        project_info_list = [{'project': project, 'remaining_days': remaining_days} for project, remaining_days in zip(projects, remaining_days_list)]

        # プロジェクトに関連付けられたタスクの数を取得してリストに追加
        task_count_list = [project.task_set.count() for project in projects]
        
        # タスクごとのworkloadを合算する。
        total_workload_list = [project.task_set.aggregate(total_workload=Sum('workload'))['total_workload'] for project in projects]

        # プロジェクト情報とタスク数、合計作業量を組み合わせてリストに追加
        for project_info, task_count, total_workload in zip(project_info_list, task_count_list, total_workload_list):
            project_info['task_count'] = task_count
            project_info['total_workload'] = total_workload

        context['project_info_list'] = project_info_list
        
        return context
    


class TaskIndex(LoginRequiredMixin,ListView):
    # 一覧するモデルを指定する -> 'object_list'で取得可能
    model = Task

    def get_queryset(self):
        if self.request.user.is_superuser:
            # スーパーユーザーはすべてのタスクを取得
            return Task.objects.all()
        else:
            # 一般ユーザーは自分のタスクのみを取得
            return Task.objects.filter(project__user=self.request.user)
        

    # データを結合させる
    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)

        tasks = self.get_queryset()

        # タスクごとの残り日数を計算してコンテキストに追加する
        # 今日の日付を抽出
        today = datetime.now().date()
        # 残り日数データを保存するリストを作成
        remaining_days_list = []
        # 各タスクの期限から今日の日付を引いて、残りに数を抽出
        for task in tasks:
            # deadlineがNullでない場合
            if task.deadline is not None:
                # 期限から今日の日付を引いて、日付として算出
                remaining_days = (task.deadline - today).days

            # deadlineがNullだった場合
            else:
                # 記号を入力
                remaining_days = "-"

            # remaing_daysをremaining_days_listに保存
            remaining_days_list.append(remaining_days)

        # タスク情報を残り日数を組み合わせてリストに追加
        task_info_list = [{'task': task, 'remaining_days': remaining_days} for task, remaining_days in zip(tasks, remaining_days_list)]

        context['task_info_list'] = task_info_list

        return context






# DetailViewは詳細を簡単に作るためのView
class DetailProject(LoginRequiredMixin,DetailView):
    # 詳細表示するモデルを指定 -> 'object'で取得可能
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 対象のプロジェクトを取得
        project = self.get_object()

        # プロジェクトの残り日数を計算
        today = datetime.now().date()
        remaining_days = "-"  # デフォルト値
        if project.deadline:
            remaining_days = (project.deadline - today).days

        # プロジェクトに関連付けられたタスクの数を取得
        task_count = project.task_set.count()

        # タスクごとのworkloadを合算する。
        # タスクごとのworkloadを合算する。
        total_workload = project.task_set.aggregate(total_workload=Sum('workload'))['total_workload'] or 0

        # コンテキストに追加
        context['project'] = project
        context['remaining_days'] = remaining_days
        context['task_count'] = task_count
        context['total_workload'] = total_workload
        
        return context

"""
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> 'object'で取得可能
    model = Task
"""


class TaskDetail(LoginRequiredMixin,DetailView):
    # 詳細表示するモデルを指定 -> 'object'で取得可能
    model = Task

    # データを結合させる
    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)

        # 対象のプロジェクトを取得
        task = self.get_object()

        # 今日の日付を抽出
        today = datetime.now().date()

        if task.deadline is not None:
            # 期限から今日の日付を引いて、日付として算出
            remaining_days = (task.deadline - today).days

            # deadlineがNullだった場合
        else:
            # 記号を入力
            remaining_days = "-"
        
        context['task'] = task
        context['remaining_days'] = remaining_days

        return context
    



class ProjectTaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'website/project_tasklist.html'  # project_tasklist.html を使用する

    def get_queryset(self):
        project_id = self.kwargs.get('pk')
        return Task.objects.filter(project_id=project_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)
        
        # プロジェクトに関連付けられたタスクの情報を取得
        tasks = Task.objects.filter(project_id=project_id)

        # タスク情報を残り日数を組み合わせてリストに追加
        today = datetime.now().date()
        remaining_days_list = []
        for task in tasks:
            if task.deadline is not None:
                remaining_days = (task.deadline - today).days
            else:
                remaining_days = "-"
            remaining_days_list.append(remaining_days)

        task_info_list = [{'task': task, 'remaining_days': remaining_days} for task, remaining_days in zip(tasks, remaining_days_list)]

        context['task_info_list'] = task_info_list
        context['project'] = project

        return context
    




# CreateViewは、新規作成画面を簡単に作るためのView
class CreateProject(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["title", "deadline", "note", "status", "user"]

    def form_valid(self, form):
        # スーパーユーザーの場合はすべてのユーザーが選択可能
        if self.request.user.is_superuser:
            form.instance.user = form.cleaned_data['user']
        else:
            # 通常のユーザーの場合はログインユーザーを設定
            form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # スーパーユーザーの場合はすべてのユーザーを選択できるようにする
        if self.request.user.is_superuser:
            form.fields['user'].queryset = User.objects.all()
    
        else:
            form.fields['user'].queryset = User.objects.filter(pk=self.request.user.pk)
        return form


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm  # カスタムフォームを指定

    # フォームにログインユーザー情報を渡す
    def get_form_kwargs(self):
        kwargs = super(CreateTask, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # ログインユーザー情報を渡す
        return kwargs



class UpdateProject(LoginRequiredMixin,UpdateView):
    template_name = "website/project_update.html"
    model = Project
    fields = ["title","deadline","note","status","user"]



class UpdateTask(LoginRequiredMixin,UpdateView):
    template_name = "website/task_update.html"
    model = Task
    fields = ["title","deadline","note","status","project", "workload","priority"]
    

class DeleteProject(LoginRequiredMixin,DeleteView):
    model = Project

    # 削除したあとに移動する先（トップページ）
    success_url = "/index"




class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task

    # 削除したあとに移動する先（トップページ）
    success_url = "/index"



def UserList(request):
    user_with_counts = User.objects.annotate(
        project_count=Count('project', distinct=True),
        task_count=Count('project__task', distinct=True)
    )
    return render(request, 'website/userlist.html', {'user_with_counts': user_with_counts})



class SignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignUpForm # 作成した登録用フォームを設定
    template_name = "website/signup.html" 
    success_url = '/index' # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)

        return response


# ログインビューを作成

class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "website/login.html"


# LogoutViewを追加
class LogoutView(BaseLogoutView):

    success_url = '/login'


