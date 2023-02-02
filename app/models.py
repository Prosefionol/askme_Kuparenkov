from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.order_by('-date')

    def get_tagged_questions(self, tag):
        return self.filter(tag__name=tag)

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

    def get_tags_by_question(self, question):
        return self.filter(question__exact=question)

    def find_by_name(self, name):
        return self.get(name__exact=name)


class ProfileManager(models.Manager):
    def find_by_user(self, user):
        return self.get(user__exact=user)

    def get_all(self):
        return self.all()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to="static/uploads/profile/")
    nick = models.CharField(max_length=25, null=True)
    objects = ProfileManager()


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
    answers = 0
    likes = 0
    objects = QuestionManager()

    def __str__(self):
        return f'Question {self.title}'


class Answer(models.Model):
    text = models.TextField()
    user = models.ForeignKey(Profile, related_name='profile_related1', on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, related_name='question_related', on_delete=models.CASCADE, blank=True, null=True)
    likes = 0
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


class AuthorizedUser:
    profile = None
    is_authorized = False
