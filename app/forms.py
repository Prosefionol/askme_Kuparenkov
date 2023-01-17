from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from app import models


class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=25)
    password = forms.CharField(min_length=1, max_length=25, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=25)
    email = forms.EmailField(required=False, max_length=25)
    nick = forms.CharField(required=False, max_length=25)
    password = forms.CharField(min_length=1, max_length=25, widget=forms.PasswordInput)
    repeat_password = forms.CharField(min_length=1, max_length=25, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if password != repeat_password:
            raise ValidationError("Passwords don't match")
        if models.User.objects.filter(username=username):
            raise ValidationError("This username is already used")
        return self.cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        nick = cleaned_data['nick']
        cleaned_data.pop('nick')
        cleaned_data.pop('repeat_password')
        cleaned_data.pop('avatar')
        user = models.User.objects.create_user(**cleaned_data)
        profile = models.Profile(user=user, nick=nick)
        profile.save()
        return profile


class AskForm(forms.Form):
    title = forms.CharField(max_length=25)
    text = forms.CharField(max_length=200, widget=forms.Textarea)
    tags = forms.CharField(max_length=200)

    def ask(self):
        question = models.Question.objects.create(
            user=models.AuthorizedUser.profile,
            title=self.cleaned_data['title'],
            text=self.cleaned_data['text'],
            date=datetime.today()
        )
        tags = self.cleaned_data["tags"]
        for tag in tags.split(", "):
            print(tag)
            if len(tag) < 25:
                if models.Tag.objects.filter(name=tag):
                    t_model = models.Tag.objects.find_by_name(tag)
                    question.tag.add(t_model)
                else:
                    t_model = models.Tag.objects.create(name=tag)
                    question.tag.add(t_model)
        return question.id


class AnswerForm(forms.Form):
    text = forms.CharField(max_length=200, widget=forms.Textarea)

    def respond(self, question_id):
        models.Answer.objects.create(
            text=self.cleaned_data['text'],
            user=models.AuthorizedUser.profile,
            question=models.Question.objects.find_by_id(question_id)
        )
