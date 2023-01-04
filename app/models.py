from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class QuestionManager(models.Manager):
    def get_hot_questions(self):
        return self.order_by('likes')

    def get_new_questions(self):
        return self.order_by('-date')

    def get_tagged_questions(self, tag):
        return self.filter(tag__exact=tag)

    def get_questions(self):
        return self.all()

    def find_by_id(self, id):
        try:
            vote = self.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404
        return vote


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question__exact=question)

    def get_answers_count(self, question):
        return self.filter(question__exact=question).count()


class TagManager(models.Manager):
    def get_all(self):
        return self.all()

    def find_by_id(self, id):
        try:
            vote = self.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404
        return vote


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to="uploads/profile/")


class Tag(models.Model):
    name = models.CharField(max_length=25)
    objects = TagManager()

    def __str__(self):
        return f'Tag {self.name}'


class Question(models.Model):
    title = models.CharField(max_length=25)
    text = models.TextField(max_length=200)
    tag = models.ManyToManyField(Tag)
    user = models.ForeignKey(Profile, related_name='profile_related', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    objects = QuestionManager()

    def __str__(self):
        return f'Question {self.title}'


class Answer(models.Model):
    text = models.TextField()
    user = models.ForeignKey(Profile, related_name='profile_related1', on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, related_name='question_related', on_delete=models.CASCADE, blank=True, null=True)
    objects = AnswerManager()


class LikeQuestionManager(models.Manager):
    def get_questions_likes(self, question):
        return self.filter(question__exact=question).count()


class LikeQuestion(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    question = models.ForeignKey(Question, models.CASCADE)

    objects = LikeQuestionManager()


class LikeAnswerManager(models.Manager):
    def get_answers_likes(self, answer):
        return self.filter(answer__exact=answer).count()


class LikeAnswer(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    answer = models.ForeignKey(Answer, models.CASCADE)

    objects = LikeAnswerManager()


# Konstrukcii dlya dz2 ostavim na vsyakiy sluchai
"""QUESTIONS = [
    {
        'id': question_id,
        'title': f'Qustion {question_id}',
        'text': f'Text voprosa nomer {question_id}',
        'answers': question_id % 2,
        'likes': question_id % 5,
        'tags': ['tag' for i in range(question_id % 3)],
        'img': f'img/avatar-{(question_id % 3) + 1}.jpg'
    } for question_id in range(10)
]


ANSWERS = [
    {
        'id': answer_id,
        'text': f'Text otveta nomer {answer_id}',
        'likes': answer_id % 5,
        'img': f'img/avatar-{(answer_id % 3) + 1}.jpg'
    } for answer_id in range(5)
]"""
