from django.contrib import admin

from game.models import Book, Question, Choice


class ChoicesInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoicesInline]


admin.site.register(Book)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
