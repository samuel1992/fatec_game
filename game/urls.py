from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('play/<int:book_id>', views.play, name='play')
]
