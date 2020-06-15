from django.contrib import admin
from django.contrib.auth.models import Group

from game.models import Book, Question, Choice, Answer


class GameModelAdmin(admin.ModelAdmin):
    def save_model(self, request=None, obj=None, form=None, change=None):
        obj.user = request.user
        obj.last_modifield_by = request.user
        obj.save()


class BookAdmin(GameModelAdmin):
    exclude = ('user',)
    list_display = ('title', 'description', 'user')


class AnswerAdmin(GameModelAdmin):
    exclude = ('user',)
    list_display = ('choice', 'question', 'is_correct', 'user')
    list_filter = ('user', 'choice')


class ChoicesInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(GameModelAdmin):
    inlines = [ChoicesInline]
    exclude = ('user',)
    list_display = ('text', 'book', 'pub_date', 'level', 'user')
    list_filter = ('text', 'book', 'user')


admin.site.site_header = 'Gameficação na leitura'
admin.site.register(Book, BookAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.unregister(Group)
