from django.shortcuts import render

from game.models import Book


def index(request):
    books = Book.objects.all()
    context = {'books': books}

    return render(request, 'game/home.html', context)


def play(request, book_id):
    context = {}
    return render(request, 'game/play.html', context)
