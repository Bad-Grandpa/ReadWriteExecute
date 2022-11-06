from django.test import TestCase
from .models import FlashCard, Lesson, Category


class LearnTestCase(TestCase):
    def setUp(self):
        categ = Category.objects.create(category_name="Animals")
        dog = FlashCard.objects.create(english_text="dog", japanese_text="inu", category=categ)
        cat = FlashCard.objects.create(english_text="cat", japanese_text="neko", category=categ)
        animal_lesson = Lesson.objects.create(lesson_name="Animal Lesson")
        animal_lesson.flash_cards.set(FlashCard.objects.all())
        bird = FlashCard.objects.create(english_text="bird", japanese_text="tori", category=categ)

    def test_lesson_created(self):
        #pulling data from setup
        animal_dog = FlashCard.objects.get(english_text="dog")
        animal_cat = FlashCard.objects.get(english_text="cat")
        animal_bird = FlashCard.objects.get(english_text="bird")
        animals_lesson = Lesson.objects.get(lesson_name="Animal Lesson")
        #checking if lesson was created according to setup
        self.assertNotEqual(list(animals_lesson.flash_cards.all()), list(FlashCard.objects.all()))
        self.assertEqual(len(list(animals_lesson.flash_cards.all())), 2)
        self.assertFalse(animal_bird in list(animals_lesson.flash_cards.all()))
        self.assertTrue(animal_dog in list(animals_lesson.flash_cards.all()))
        self.assertTrue(animal_cat in list(animals_lesson.flash_cards.all()))

