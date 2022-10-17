from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Category, FlashCard

# Create your views here.


def index(request):
    context = {'navbar': 'home'}
    return render(request, 'learnjapanese/index.html', context)


class CategoriesView(generic.ListView):
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'category'
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return FlashCard.objects.filter(category__pk=self.kwargs['pk'])


class AboutView(generic.TemplateView):
    template_name = 'learnjapanese/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'about'
        return context
