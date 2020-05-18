from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, related_name='player',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    answered_books = models.IntegerField(default=0)


class Book(models.Model):
    title = models.CharField(max_length=100)


class Question(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, blank=False)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)


class Choice(models.Model):
    text = models.CharField(max_length=200)
    right = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
