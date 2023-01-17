from django.contrib import auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from . import models, forms
from operator import attrgetter
from django.http import HttpResponse

t_list = models.Tag.objects.get_all()
p_list = models.Profile.objects.get_all()
saved_path = ""


def set_parameters(q_list):
    for q in q_list:
        q.answers = models.Answer.objects.get_answers_count(q)
        q.likes = models.LikeQuestion.objects.get_questions_likes(q)
    return q_list


def index(request):
    q_list = models.Question.objects.get_new_questions()
    q_list = set_parameters(q_list)
    context = {'questions': q_list, 'page_obj': listing(request, q_list), 'tags': t_list,
               'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser}
    return render(request, 'index.html', context=context)


def hotq(request):
    q_list = models.Question.objects.get_questions()
    q_list = set_parameters(q_list)
    q_list = sorted(q_list, key=attrgetter('likes'))
    q_list.reverse()
    context = {'questions': q_list, 'page_obj': listing(request, q_list), 'tags': t_list,
               'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser}
    return render(request, 'hotq.html', context=context)


def question(request, question_id: int):
    context = {}
    if request.method == "GET":
        form = forms.AnswerForm()

    if request.method == "POST":
        if not models.AuthorizedUser.is_authorized:
            return redirect(reverse("login"))
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            form.respond(question_id)
            return redirect(reverse('question', args=[question_id]))
        context.update({'Invalid': True, 'Exception': form.errors})
        print(form.errors)

    question_item = models.Question.objects.find_by_id(question_id)
    question_item.answers = models.Answer.objects.get_answers_count(question_item)
    question_item.likes = models.LikeQuestion.objects.get_questions_likes(question_item)
    answs = models.Answer.objects.get_answers(question_item)
    for answer in answs:
        answer.likes = models.LikeAnswer.objects.get_answers_likes(answer)
    context.update({'form': form})
    context.update({'question': question_item, 'answers': answs, 'page_obj': listing(request, answs),
                    'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser})
    return render(request, 'question.html', context=context)


def tag(request, tag_id: str):
    q_list = models.Question.objects.get_tagged_questions(tag_id)
    q_list = set_parameters(q_list)
    context = {'questions': q_list, 'page_obj': listing(request, q_list), 'tags': t_list, 't_id': tag_id,
               'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser}
    return render(request, 'tag.html', context=context)


def ask(request):
    context = {'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser}
    if not models.AuthorizedUser.is_authorized:
        return redirect(reverse("login"))
    if request.method == "GET":
        form = forms.AskForm()
    if request.method == "POST":
        form = forms.AskForm(request.POST)
        if form.is_valid():
            return redirect(reverse('question', args=[form.ask()]))
        context.update({'Invalid': True, 'Exception': form.errors})
    context.update({'form': form})
    return render(request, 'ask.html', context=context)


def login(request):
    global saved_path
    context = {'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser}
    if request.method == "GET":
        form = forms.LoginForm()
        path = request.META.get('HTTP_REFERER')[22:]
        saved_path = path
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                models.AuthorizedUser.profile = models.Profile.objects.find_by_user(user)
                models.AuthorizedUser.is_authorized = True
                if saved_path == "":
                    return redirect(reverse("index"))
                else:
                    if saved_path[0] == 'q':
                        number = int(saved_path[9:])
                        return redirect(reverse("question", args=[number]))
                    else:
                        if saved_path[0] == 't':
                            return redirect(reverse("tag", args=[saved_path[4:]]))
                        else:
                            return redirect(reverse(saved_path))
            else:
                form.add_error(None, 'Invalid username or password!')
                context.update({'Invalid': True, 'Exception': form.errors, 'form': form})
                print(form.errors)
    context.update({'form': form})
    return render(request, 'login.html', context=context)


def logout(request):
    models.AuthorizedUser.profile = None
    models.AuthorizedUser.is_authorized = False
    return redirect(reverse("index"))


def register(request):
    context = {'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser}
    if request.method == "GET":
        form = forms.RegisterForm()
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            profile = form.save()
            if profile:
                models.AuthorizedUser.profile = profile
                models.AuthorizedUser.is_authorized = True
                return redirect(reverse("index"))
            else:
                form.add_error(None, 'Invalid data error!')
                context.update({'Invalid': True, 'Exception': form.errors})
    context.update({'form': form})
    return render(request, 'register.html', context=context)


def settings(request):
    context = {'pop_tags': t_list[:5], 'best_users': p_list[:5], 'auth_user': models.AuthorizedUser}
    return render(request, 'settings.html', context=context)


def listing(request, pagList):
    contact_list = pagList
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
