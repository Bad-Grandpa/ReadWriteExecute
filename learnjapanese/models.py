from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class FlashCard(models.Model):
    english_text = models.CharField(max_length=100)
    japanese_text = models.CharField(max_length=100)
    japanese_text_kanji = models.CharField(max_length=100, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.english_text


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100)
    flash_cards = models.ManyToManyField(FlashCard)

    def __str__(self):
        return self.lesson_name

    def get_absolute_url(self):
        return reverse('learnjapanese:lesson_single', kwargs={'pk': self.pk})
