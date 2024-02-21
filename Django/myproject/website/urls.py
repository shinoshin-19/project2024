from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # path('', IndexView.as_view()),
    path('', views.TopIndex.as_view(),name = "index"),
    path('user', views.UserIndex.as_view(),name = "user"),
    path('project', views.ProjectIndex.as_view(),name = "project_list"),
    path('task', views.TaskIndex.as_view(),name = "task_list"),
    # <pk>にTaskのIDを渡すと表示される。
    # path('detail/<pk>',views.Detail.as_view(),name = "detail"),
    path('detailtask/<pk>',views.TaskDetail.as_view(),name = "detailtask"),
    path('project/<pk>',views.DetailProject.as_view(),name = "detailproject"),
    path('createproject/',views.CreateProject.as_view(), name = "createproject"),
    path('create/',views.Create.as_view(), name = "create"),
    path('update/<pk>',views.Update.as_view(), name = "update"),
    path('delete/<pk>',views.Delete.as_view(), name = "delete"),
    path('userlist',views.UserList,name = "userlist"),
    # プロジェクトのIDを渡して、そのプロジェクトに関連付けられたタスクを表示するURL
    path('project/<pk>/taskslist/', ProjectTaskListView.as_view(),name='project_tasklist'),

]