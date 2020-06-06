from django.test import TestCase

from game.models import Book, Question, Choice, Answer, User
from game.views import index, questions, play


class BookTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='123456')
        self.book = Book.objects.create(title='test_1',
                                        author='samuel',
                                        description='teste de descricao',
                                        user=user)

    def test_book_representation(self):
        self.assertEqual(str(self.book), self.book.title)


class QuestionTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='123456')
        book = Book.objects.create(title='test_1',
                                   author='samuel',
                                   description='teste de descricao',
                                   user=user)
        self.question = Question.objects.create(book=book,
                                                user=user,
                                                text='teste questao')

    def test_question_representation(self):
        self.assertEqual(str(self.question), self.question.text)


class ChoiceTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='123456')
        book = Book.objects.create(title='test_1',
                                   author='samuel',
                                   description='teste de descricao',
                                   user=user)
        question = Question.objects.create(book=book,
                                           user=user,
                                           text='teste questao')
        self.choice = Choice.objects.create(question=question,
                                            correct=False,
                                            text='teste')

    def test_choice_representation(self):
        self.assertEqual(str(self.choice), self.choice.text)


class AnswerTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='samuel', password='123456')
        self.book = Book.objects.create(title='Genealogia da Moral',
                                        author='Nietzsche',
                                        description='Uma descrição',
                                        user=user)
        self.question = Question.objects.create(book=self.book,
                                                user=user,
                                                text='Uma pergunta')
        self.choice_1 = Choice.objects.create(question=self.question,
                                              correct=False,
                                              text='Uma possível resposta')
        self.choice_2 = Choice.objects.create(question=self.question,
                                              correct=True,
                                              text='Outra resposta')

    def test_incorrect_answer(self):
        answer = Answer.objects.create(choice=self.choice_1)
        self.assertEqual(answer.is_correct(), False)

    def test_correct_answer(self):
        answer = Answer.objects.create(choice=self.choice_2)
        self.assertEqual(answer.is_correct(), True)

    def test_return_related_question(self):
        answer = Answer.objects.create(choice=self.choice_1)
        self.assertEqual(answer.question, self.question)

    def test_return_related_book(self):
        answer = Answer.objects.create(choice=self.choice_1)
        self.assertEqual(answer.book, self.book)

    def test_answer_representarion(self):
        answer = Answer.objects.create(choice=self.choice_1)
        self.assertEqual(str(answer), answer.choice.text)


class IndexViewTest(TestCase):
    def test_get(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/home.html')


class QuestionsViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='samuel', password='123456')
        self.book = Book.objects.create(title='Genealogia da Moral',
                                        author='Nietzsche',
                                        description='Uma descrição',
                                        user=user)

    def test_get(self):
        response = self.client.get(f'/questions/{self.book.id}', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/questions.html')


class PlayViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='samuel', password='123456')
        book = Book.objects.create(title='Genealogia da Moral',
                                   author='Nietzsche',
                                   description='Uma descrição',
                                   user=user)
        self.question = Question.objects.create(book=book,
                                                user=user,
                                                text='teste questao')

    def test_get(self):
        response = self.client.get(f'/questions/play/{self.question.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/play.html')

    def test_post(self):
        payload = {'choice': 1}
        response = self.client.post(f'/questions/play/{self.question.id}',
                                    payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/check_answer.html')
