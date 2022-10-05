from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Category

# Create your views here.


def index(request):
    return HttpResponse("Welcome to the index page!")


class CategoriesView(generic.ListView):
    template_name = 'learnjapanese/categories.html'

    def get_queryset(self):
        return Category.objects.order_by('-category_name')


class CategoryView(generic.ListView):
    template_name = 'learnjapanese/category.html'

    def get_queryset(self):
        pass
