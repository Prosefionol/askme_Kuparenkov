from django.shortcuts import render
from . import models
from django.http import HttpResponse


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    if question_id >= len(models.QUESTIONS):
        context_a = {'maxsize': len(models.QUESTIONS)}
        return render(request, 'error.html', context=context_a)
    else:
        question_item = models.QUESTIONS[question_id]
        context_b = {'question': question_item, 'answers': models.ANSWERS}
        return render(request, 'question.html', context=context_b)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
