from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return f'{self.text} ({self.book.title})'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    correct = models.BooleanField()

    def __str__(self):
        return f'{self.choice}'
