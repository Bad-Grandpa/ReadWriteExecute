from django.http import HttpResponse
from django.views import generic, View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from .models import Category, FlashCard, Lesson
from .util.lesson_util import add_two_random_fcs


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


class TrainLessonView(generic.TemplateView):
    template_name = 'learnjapanese/lesson_train.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'lesson'

        context['lesson'] = Lesson.objects.get(pk=self.kwargs.get('pk'))
        question_no = context['question'] - 1
        question_pk_list = self.request.session.get('training_question_list')
        question_pk = question_pk_list[question_no]
        context['question_obj'] = FlashCard.objects.get(pk=question_pk)
        context['answers'] = [FlashCard.objects.get(pk=answer_pk)
            for answer_pk in self.request.session['training_answer_list'][question_no]]
 
        return context
    

class TrainLessonStartView(View):
    def get(self, request, *args, **kwargs):
        '''
        Initiate training parameters in session. That includes:
        - current training id
        - last question number (0 in start view)
        - question FlashCards pks list
        - answer FlashCards pks list (list of tuples)
        - current score
        '''
        lesson_obj = Lesson.objects.get(pk=kwargs.get('pk'))
        request.session['training_id'] = kwargs.get('pk')
        request.session['training_last_question'] = 0
        
        question_list =[flashcard.id for flashcard in lesson_obj.flash_cards.all()]
        request.session['training_question_list'] = question_list
        request.session['training_answer_list'] = [add_two_random_fcs(pk) for pk in question_list]
        request.session['training_score'] = 0

        url_params = {
            'pk': request.session['training_id'],
            'question': request.session['training_last_question'] + 1,
        }
        return redirect(reverse('learnjapanese:lesson_tr', kwargs=url_params))


class TrainLessonSubmitAnswer(View):
    def get(self, request, *args, **kwargs):
        lesson_pk = kwargs.get('pk')
        answer_no = kwargs.get('answer')
        question_no = kwargs.get('question')

        # check if submit is legitimate
        if (request.session.get('training_last_question') + 1) != question_no or \
            request.session.get('training_id') != lesson_pk:
            # TODO redirect to cheat view
            pass

        # update score
        question_list = request.session['training_question_list']
        answer_list = request.session['training_answer_list']

        if question_list[question_no - 1] == answer_list[question_no - 1][answer_no]:
            request.session['training_score'] += 1
        
        # if last, redirect to results
        if question_no == len(question_list):
            url_params = {'pk': lesson_pk}
            return redirect(reverse('learnjapanese:lesson_tr_result', kwargs=url_params))
        
        # otherwise, redirect to the next question
        question_no += 1
        request.session['training_last_question'] = question_no
        url_params = {
            'pk': lesson_pk,
            'question': question_no
        }
        return redirect(reverse('learnjapanese:lesson_tr', kwargs=url_params))


class TrainLessonResultsView(generic.TemplateView):
    template_name = 'learnjapanese/lesson_train_results.html'

    def __clear_session(self):
        del self.request.session['training_id']
        del self.request.session['training_last_question']
        del self.request.session['training_question_list']
        del self.request.session['training_answer_list']
        del self.request.session['training_score']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'lesson'
        context['score'] = self.request.session['training_score']
        context['lesson'] = Lesson.objects.get(pk=self.kwargs.get('pk'))
        context['lesson_len'] = len(self.request.session['training_question_list'])

        # self.__clear_session()
        return context

class TrainLessonFailView(generic.TemplateView):
    template_name = 'learnjapanese/lesson_fail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

class SearchResultView(generic.ListView):
    model = FlashCard
    template_name = 'learnjapanese/search_results.html'
    context_object_name = 'search_results'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'lesson'
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
