from django.contrib import admin

from game.models import Player, Book, Question, Choice

admin.site.register(Player)
admin.site.register(Book)
admin.site.register(Question)
admin.site.register(Choice)
