from django.contrib import admin
from django.urls import path
from .views import IndexView
from . import views

urlpatterns = [
    # path('', IndexView.as_view()),
    path('', views.Index.as_view(),name = "task"),
    # <pk>にTaskのIDを渡すと表示される。
    path('detail/<pk>',views.Detail.as_view(),name = "detail"),
    path('create/',views.Create.as_view(), name = "create"),
    path('update/<pk>',views.Update.as_view(), name = "update"),
    path('delete/<pk>',views.Delete.as_view(), name = "delete"),
    

]