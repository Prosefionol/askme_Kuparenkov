from django.core.paginator import Paginator
from django.shortcuts import render
from . import models
from django.http import HttpResponse


def index(request):
    q_list = models.Question.objects.get_new_questions()
    context = {'questions': q_list, 'page_obj': listing(request, q_list)}
    # context = {'questions': models.Question, 'tags': models.Tag, 'page_obj': pagging(contact_list, request),
    #           'profiles': models.Profile, 'likes': models.LikeQuestion}
    return render(request, 'index.html', context=context)


def hotq(request):
    q_list = models.Question.objects.get_hot_questions()
    context = {'questions': q_list, 'page_obj': listing(request, q_list)}
    return render(request, 'hotq.html', context=context)


def question(request, question_id: int):
    if question_id >= len(models.QUESTIONS):
        context_a = {'maxsize': len(models.QUESTIONS)}
        return render(request, 'error.html', context=context_a)
    else:
        question_item = models.QUESTIONS[question_id]
        context_b = {'question': question_item, 'answers': models.ANSWERS,
                     'page_obj': listing(request, models.ANSWERS)}
        return render(request, 'question.html', context=context_b)


def tag(request, tag_id: str):
    context = {'tag': tag_id, 'questions': models.QUESTIONS, 'page_obj': listing(request, models.QUESTIONS)}
    return render(request, 'tag.html', context=context)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')


def listing(request, pagList):
    contact_list = pagList
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
