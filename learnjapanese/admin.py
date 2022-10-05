from django.contrib import admin
from .models import FlashCard, Category, Lesson

# Register your models here.

admin.site.register(FlashCard)
admin.site.register(Category)
admin.site.register(Lesson)