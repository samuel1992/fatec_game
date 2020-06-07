from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from game.models import Book, Question, Answer
from game.forms import AnswerForm


@login_required
def home(request):
    books = Book.objects.all()
    context = {'books': books}

    return render(request, 'game/home.html', context)


@login_required
def questions(request, book_id):
    book = Book.objects.get(id=book_id)
    questions = book.questions.all()
    context = {'questions': questions, 'book': book}

    return render(request, 'game/questions.html', context)


@login_required
def play(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.POST:
        form = AnswerForm(None, request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.save()

            if answer.is_correct():
                player = request.user.player.first()
                player.add_point(question, answer)

            return redirect('check_answer', answer_id=answer.id)

    form = AnswerForm(question)
    context = {'question': question, 'form': form}
    return render(request, 'game/play.html', context)


@login_required
def check_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    return render(request, 'game/check_answer.html', {'answer': answer})
