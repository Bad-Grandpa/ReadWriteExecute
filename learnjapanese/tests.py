from django.test import TestCase
from .models import FlashCard, Lesson, Category
import datetime
from django.utils import timezone

class LearnTestCase(TestCase):
    def setUp(self):
        animals = Category.objects.create(category_name="Animals")
        vehicles = Category.objects.create(category_name="Vehicles")
        dog = FlashCard.objects.create(english_text="dog", japanese_text="inu", category=animals)
        cat = FlashCard.objects.create(english_text="cat", japanese_text="neko", category=animals)
        animal_lesson = Lesson.objects.create(lesson_name="Animal Lesson")
        animal_lesson.flash_cards.set(FlashCard.objects.all())
        bird = FlashCard.objects.create(english_text="bird", japanese_text="tori", category=animals)

    def test_lesson_created(self):
        #Get data from setUp
        animal_dog = FlashCard.objects.get(english_text="dog")
        animal_cat = FlashCard.objects.get(english_text="cat")
        animal_bird = FlashCard.objects.get(english_text="bird")
        animals_lesson = Lesson.objects.get(lesson_name="Animal Lesson")
        #Checking if Lesson was created according to setUp
        self.assertNotEqual(list(animals_lesson.flash_cards.all()), list(FlashCard.objects.all()))
        self.assertEqual(len(list(animals_lesson.flash_cards.all())), 2)
        self.assertFalse(animal_bird in list(animals_lesson.flash_cards.all()))
        self.assertTrue(animal_dog in list(animals_lesson.flash_cards.all()))
        self.assertTrue(animal_cat in list(animals_lesson.flash_cards.all()))

    def test_card_created(self):
        #Get data from setUp
        animal_dog = FlashCard.objects.get(english_text="dog")
        animal_cat = FlashCard.objects.get(english_text="cat")
        animal_bird = FlashCard.objects.get(english_text="bird")
        animals_english = ["dog", "cat", "bird"]
        animals_japanese = ["inu", "neko", "tori"]
        animals_category = "Animals"
        #Checking if FlashCard was created according to setUp
        self.assertTrue(animal_bird.english_text in animals_english)
        self.assertTrue(animal_cat.english_text in animals_english)
        self.assertTrue(animal_dog.english_text in animals_english)
        self.assertTrue(animal_bird.japanese_text in animals_japanese)
        self.assertTrue(animal_cat.japanese_text in animals_japanese)
        self.assertTrue(animal_dog.japanese_text in animals_japanese)
        self.assertEqual(str(animal_bird.category), animals_category)
        self.assertLess(animal_dog.creation_date, timezone.now())

    def test_category_created(self):
        #Get data from setUp
        animals_category = Category.objects.get(category_name="Animals")
        vehicles_category = Category.objects.get(category_name="Vehicles")
        category_as_string = "Animals"
        #Checking if Category was created according to setUp
        self.assertEqual(animals_category.category_name, category_as_string)
        self.assertNotEqual(animals_category.category_name, vehicles_category.category_name)
    

