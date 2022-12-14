import datetime
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from .models import *
from .views import *


class LearnTestCase(TestCase):
    def setUp(self):
        self.kwargs = {'pk':1}
        self.kwargs_pk_question = {'pk':1, 'question':1}
        self.kwargs_pk_question_answer = {'pk':1, 'question':1, 'answer':1}
        self.client = Client()
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

    def test_about_view_response(self):
        response = self.client.get(reverse("learnjapanese:about"))
        self.assertEqual(response.status_code, 200)

    def test_lesson_list_view_response(self):
        response = self.client.get(reverse("learnjapanese:lessons_list"))
        self.assertEqual(response.status_code, 200)

    def test_lesson_create_view_response(self):
        response = self.client.get(reverse("learnjapanese:lesson_create"))
        self.assertEqual(response.status_code, 200)

    def test_lesson_single_view_response(self):
        response = self.client.get(reverse("learnjapanese:lesson_single", kwargs=self.kwargs))
        self.assertEqual(response.status_code, 200)

    def test_category_view_response(self):
        response = self.client.get(reverse("learnjapanese:categories_list"))
        self.assertEqual(response.status_code, 200)

    def test_category_single_view_response(self):
        response = self.client.get(reverse("learnjapanese:category_single", kwargs=self.kwargs))
        self.assertEqual(response.status_code, 200)

    def test_lessson_train_start_view_response(self):
        response = self.client.get(reverse("learnjapanese:lesson_tr_start", kwargs=self.kwargs))
        #since it is a redirect we expect a 302
        self.assertEqual(response.status_code, 302)

    def test_lessson_train_view_response(self):
        #we run a page to create session for training
        self.client.get(reverse("learnjapanese:lesson_tr_start", kwargs=self.kwargs))
        response = self.client.get(reverse("learnjapanese:lesson_tr", kwargs=self.kwargs_pk_question))
        self.assertEqual(response.status_code, 200)

    def test_lesson_train_submit(self):
        #again we are being redirected to next question
        self.client.get(reverse("learnjapanese:lesson_tr_start", kwargs=self.kwargs))
        self.client.get(reverse("learnjapanese:lesson_tr", kwargs=self.kwargs_pk_question))
        response = self.client.get(reverse("learnjapanese:lesson_tr_submit", kwargs=self.kwargs_pk_question_answer))
        self.assertEqual(response.status_code, 302)

    def test_lesson_train_result_view(self):
        session = self.client.session
        session['training_id'] = 1
        session['training_last_question'] = 3
        session['training_question_list'] = [_ for _ in range(3)]
        session['training_answer_list'] = [_ for _ in range(3)]
        session['training_score'] = 3
        session.save()
        response = self.client.get(reverse("learnjapanese:lesson_tr_result", kwargs=self.kwargs))
        self.assertEqual(response.status_code, 200)
        # example of assertContains
        self.assertContains(response, "3 out of 3")
