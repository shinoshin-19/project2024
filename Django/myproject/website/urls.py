from django.contrib import admin
from django.urls import path
from .views import *
from . import views


urlpatterns = [
    # path('', IndexView.as_view()),
    path('index', views.TopIndex.as_view(), name="index"),
    path('user', views.UserIndex.as_view(),name = "user"),
    path('project', views.ProjectIndex.as_view(),name = "project_list"),
    path('task', views.TaskIndex.as_view(),name = "task_list"),
    # <pk>にTaskのIDを渡すと表示される。
    # path('detail/<pk>',views.Detail.as_view(),name = "detail"),
    path('detailtask/<pk>',views.TaskDetail.as_view(),name = "detailtask"),
    path('project/<pk>',views.DetailProject.as_view(),name = "detailproject"),
    path('createproject/',views.CreateProject.as_view(), name = "createproject"),
    path('createtask/',views.CreateTask.as_view(), name = "createtask"),
    path('updatetask/<pk>',views.UpdateTask.as_view(), name = "updatetask"),
    path('deletetask/<pk>',views.DeleteTask.as_view(), name = "deletetask"),
    path('updateproject/<pk>',views.UpdateProject.as_view(), name = "updateproject"),
    path('deleteproject/<pk>',views.DeleteProject.as_view(), name = "deleteproject"),
    path('userlist',views.UserList,name = "userlist"),
    # プロジェクトのIDを渡して、そのプロジェクトに関連付けられたタスクを表示するURL
    path('project/<pk>/taskslist/', ProjectTaskListView.as_view(),name='project_tasklist'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    

]