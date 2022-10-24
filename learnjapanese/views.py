from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Category, FlashCard, Lesson


# Create your views here.


def index(request):
    context = {'navbar': 'home'}
    return render(request, 'learnjapanese/index.html', context)


class CategoryListView(generic.ListView):
    template_name = 'learnjapanese/categories.html'

    def get_queryset(self):
        return Category.objects.order_by('category_name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'category'
        return context


class CategoryView(generic.ListView):
    template_name = 'learnjapanese/category.html'
    context_object_name = 'flashcards_by_category'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'category'
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return FlashCard.objects.filter(category__pk=self.kwargs['pk']).order_by('english_text')


class LessonListView(generic.ListView):
    model = Lesson
    template_name = 'learnjapanese/lessons.html'
    context_object_name = 'lessons'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'lesson'
        return context


class LessonCreateView(generic.CreateView):
    model = Lesson
    template_name = 'learnjapanese/lesson_create.html'
    fields = ['lesson_name', 'flash_cards']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'lesson'
        return context


class AboutView(generic.TemplateView):
    template_name = 'learnjapanese/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'about'
        return context


def todo_view(request):
    return render(request, 'learnjapanese/todo.html', {})
