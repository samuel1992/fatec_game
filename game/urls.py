from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('questions/<int:book_id>', views.questions, name='questions'),
    path('questions/play/<int:question_id>', views.play, name='play'),
    path('check_answer/<int:answer_id>',
         views.check_answer, name='check_answer'),
    path('accounts/', include('django.contrib.auth.urls')),
]
