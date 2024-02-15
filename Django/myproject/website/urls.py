from django.contrib import admin
from django.urls import path
from .views import IndexView
from . import views

urlpatterns = [
    # path('', IndexView.as_view()),
    path('user', views.UserIndex.as_view(),name = "user"),
    path('project', views.ProjectIndex.as_view(),name = "project_list"),
    path('', views.Index.as_view(),name = "task"),
    # <pk>にTaskのIDを渡すと表示される。
    path('detail/<pk>',views.Detail.as_view(),name = "detail"),
    path('detailproject/<pk>',views.DetailProject.as_view(),name = "detailproject"),
    path('createproject/',views.CreateProject.as_view(), name = "createproject"),
    path('create/',views.Create.as_view(), name = "create"),
    path('update/<pk>',views.Update.as_view(), name = "update"),
    path('delete/<pk>',views.Delete.as_view(), name = "delete"),
    path('userlist',views.UserList,name = "userlist"),

]