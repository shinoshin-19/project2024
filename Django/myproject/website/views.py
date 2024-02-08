from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView 
from .models import *
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView


class IndexView(TemplateView):
    template_name = "index.html"

# ListViewは、一覧を簡単に作るためのView
class Index(ListView):
    # 一覧するモデルを指定する -> 'object_list'で取得可能
    model = Task

# DetailViewは詳細を簡単に作るためのView
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> 'object'で取得可能
    model = Task

# CreateViewは、新規作成画面を簡単に作るためのView
class Create(CreateView):
    model = Task

    # 編集対象にするフィールド
    fields = ["name","deadline","note","status","project"]

class Update(UpdateView):
    model = Task
    fields = ["name","deadline","note","status","project"]
    

class Delete(DeleteView):
    model = Task

    # 削除したあとに移動する先（トップページ）
    success_url = "/"