from django.test import TestCase

from game.models import Book, Question, Choice, Answer, User


class BookTest(TestCase):
    def setUp(self):
        myuser = User.objects.first()
        Book.objects.create(title='test_1', author='samuel',
                            description='teste de descricao', user=myuser)

    def test_book_exists(self):
        book = Book.objcts.get(name='test_1')
        self.assertIsNotNone(book)
