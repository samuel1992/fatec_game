from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('questions/<int:book_id>', views.questions, name='questions'),
    path('questions/play/<int:question_id>', views.play, name='play'),
    path('check_answer/<int:answer_id>',
         views.check_answer, name='check_answer'),
]
