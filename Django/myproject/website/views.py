from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView 
from .models import *
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime



class IndexView(TemplateView):
    template_name = "index.html"

# ListViewは、一覧を簡単に作るためのView
class UserIndex(ListView,):
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
    



class ProjectIndex(ListView):
    # 一覧するモデルを指定する -> 'object_list'で取得可能
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # プロジェクトの一覧を取得
        projects = Project.objects.all()

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

        # プロジェクト情報とタスク数を組み合わせてリストに追加
        for project_info, task_count in zip(project_info_list, task_count_list):
            project_info['task_count'] = task_count

        context['project_info_list'] = project_info_list
        
        return context
    



class Index(ListView):
    # 一覧するモデルを指定する -> 'object_list'で取得可能
    model = Task

# DetailViewは詳細を簡単に作るためのView
class DetailProject(DetailView):
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

        # コンテキストに追加
        context['project'] = project
        context['remaining_days'] = remaining_days
        context['task_count'] = task_count
        
        return context








class Detail(DetailView):
    # 詳細表示するモデルを指定 -> 'object'で取得可能
    model = Task

# CreateViewは、新規作成画面を簡単に作るためのView

class CreateProject(CreateView):
    model = Project

    # 編集対象にするフィールド
    fields = ["title","deadline","note","status","user"]


class Create(CreateView):
    model = Task

    # 編集対象にするフィールド
    fields = ["title","deadline","note","status","project"]

class Update(UpdateView):
    model = Task
    fields = ["title","deadline","note","status","project"]
    

class Delete(DeleteView):
    model = Task

    # 削除したあとに移動する先（トップページ）
    success_url = "/"

def UserList(request):
    user_with_counts = User.objects.annotate(
        project_count=Count('project', distinct=True),
        task_count=Count('project__task', distinct=True)
    )
    return render(request, 'website/userlist.html', {'user_with_counts': user_with_counts})