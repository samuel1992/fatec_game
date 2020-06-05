from django.shortcuts import render

from game.models import Book, Question, Choice
from game.forms import AnswerForm


def index(request):
    books = Book.objects.all()
    context = {'books': books}

    return render(request, 'game/home.html', context)


def questions(request, book_id):
    book = Book.objects.get(id=book_id)
    questions = book.questions.all()
    context = {'questions': questions, 'book': book}

    return render(request, 'game/questions.html', context)


def play(request, question_id):
    if request.POST:
        form = AnswerForm(None, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'game/check_answer.html', {'answer':
                                                              form.instance})

    question = Question.objects.get(id=question_id)
    form = AnswerForm(question=question)
    context = {'question': question, 'form': form}
    return render(request, 'game/play.html', context)
