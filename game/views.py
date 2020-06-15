from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDay

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


@login_required
def dashboard(request):
    book_by_author = Book.objects.values('author').annotate(Count('id'))
    answer_by_book = Answer.objects.values('choice__question__book__title')\
        .annotate(Count('id'))
    answer_by_user = Answer.objects.values('user__username')\
        .annotate(Count('id'))
    answer_by_date = Answer.objects \
        .annotate(month=TruncDay('pub_date')) \
        .values('pub_date') \
        .annotate(Count('id'))

    context = {
        'book_by_author': book_by_author,
        'answer_by_book': answer_by_book,
        'answer_by_user': answer_by_user,
        'answer_by_date': answer_by_date
    }
    return render(request, 'game/dashboard.html', context)
