from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, FlashCard, Lesson


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
    paginate_by = 15

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


class LessonDetailView(generic.DetailView):
    model = Lesson
    template_name = 'learnjapanese/lesson.html'
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'lesson'
        return context


class LessonTrainView(generic.DetailView):
    model = Lesson
    template_name = 'learnjapanese/lesson_train.html'
    context_object_name = "lesson"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'lesson'
        return context


class SearchResultView(generic.ListView):
    model = FlashCard
    template_name = 'learnjapanese/search_results.html'
    context_object_name = 'search_results'
    paginate_by = 16

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        return FlashCard.objects.filter(Q(english_text__icontains=query) | Q(japanese_text__icontains=query))


class AboutView(generic.TemplateView):
    template_name = 'learnjapanese/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'about'
        return context


def todo_view(request, pk=None):
    return render(request, 'learnjapanese/todo.html', {})
