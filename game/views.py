from django.shortcuts import render, redirect

from game.models import Book, Question, Choice, Answer
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
            return redirect('check_answer', answer_id=form.instance.id)

    question = Question.objects.get(id=question_id)
    form = AnswerForm(question=question)
    context = {'question': question, 'form': form}
    return render(request, 'game/play.html', context)


def check_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    return render(request, 'game/check_answer.html', {'answer': answer})
