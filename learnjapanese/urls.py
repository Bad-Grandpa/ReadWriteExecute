from django.urls import path

from . import views

app_name = 'learnjapanese'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.CategoryListView.as_view(), name='categories_list'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category_single'),
    path('lesson/', views.LessonListView.as_view(), name='lessons_list'),
    path('lesson/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>', views.LessonDetailView.as_view(), name='lesson_single'),
    path('lesson/<int:pk>/train/', views.LessonTrainStartView.as_view(), name='lesson_train_start'),
    path('lesson/<int:pk>/train/<int:question>', views.LessonTrainView.as_view(), name='train'),
    path('lesson/<int:pk>/train/<int:question>/submit/<int:answer>', views.todo_view, name='lesson_train_submit'),
    path('lesson/<int:pk>/train/result', views.todo_view, name='train_result'),
    path('search/', views.SearchResultView.as_view(), name='flashcard_search'),
    path('about/', views.AboutView.as_view(), name='about'),
]
