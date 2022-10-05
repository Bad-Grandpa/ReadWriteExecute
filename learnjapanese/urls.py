from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.CategoriesView.as_view(), name='categories_list'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='single category')
]