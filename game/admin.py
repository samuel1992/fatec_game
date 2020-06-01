from django.contrib import admin
from django.contrib.auth.models import Group

from game.models import Book, Question, Choice


class BookAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('title', 'description', 'user')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.last_modifield_by = request.user
        obj.save()


class ChoicesInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoicesInline]
    exclude = ('user',)
    list_display = ('text', 'book', 'pub_date', 'user')
    list_filter = ('text', 'book', 'user')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.last_modifield_by = request.user
        obj.save()


admin.site.site_header = 'Gameficação na leitura'
admin.site.register(Book, BookAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.unregister(Group)
