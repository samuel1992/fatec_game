from django.db import models
from django.contrib.auth.models import User

CHOICE_VALUE = 2


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return f'{self.text}'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='choices')
    correct = models.BooleanField()
    text = models.CharField(max_length=200)

    @property
    def value(self):
        return CHOICE_VALUE

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='answers')

    def is_correct(self):
        return self.choice.correct

    @property
    def question(self):
        return self.choice.question

    @property
    def book(self):
        return self.choice.question.book

    def __str__(self):
        return f'{self.choice}'

    def __len__(self):
        return Answer.objects.filter(user=self.user,
                                     choice__question=self.question).count()


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='player')

    def add_point(self, question, answer):
        Point.objects.create(player=self, question=question, answer=answer)


class Point(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,
                               related_name='points')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __remove_choices_by_qtd_of_wrong_answers(self, wrong_answers):
        """each choice has an configurable value, the rule is:
        for each wrong attempt answer the player lost a point value equivalent
        to one choice
        """
        return self.question.choices.all()[wrong_answers::]

    @property
    def value(self):
        wrong_answers = len(self.answer) - 1
        choices = self.__remove_choices_by_qtd_of_wrong_answers(wrong_answers)

        return sum(i.value for i in choices)
