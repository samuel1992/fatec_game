from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from game.models import Book, Question, Choice, Answer, User, Player
from game.admin import BookAdmin
from game.apps import GameConfig

CHOICE_VALUE = 2


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

    def test_choice_value(self):
        self.assertEqual(self.choice.value, CHOICE_VALUE)


class AnswerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='samuel',
                                             password='123456')
        self.book = Book.objects.create(title='Genealogia da Moral',
                                        author='Nietzsche',
                                        description='Uma descrição',
                                        user=self.user)
        self.question = Question.objects.create(book=self.book,
                                                user=self.user,
                                                text='Uma pergunta')
        self.choice_1 = Choice.objects.create(question=self.question,
                                              correct=False,
                                              text='Uma possível resposta')
        self.choice_2 = Choice.objects.create(question=self.question,
                                              correct=True,
                                              text='Outra resposta')

    def test_incorrect_answer(self):
        answer = Answer.objects.create(choice=self.choice_1, user=self.user)
        self.assertEqual(answer.is_correct(), False)

    def test_correct_answer(self):
        answer = Answer.objects.create(choice=self.choice_2, user=self.user)
        self.assertEqual(answer.is_correct(), True)

    def test_return_related_question(self):
        answer = Answer.objects.create(choice=self.choice_1, user=self.user)
        self.assertEqual(answer.question, self.question)

    def test_return_related_book(self):
        answer = Answer.objects.create(choice=self.choice_1, user=self.user)
        self.assertEqual(answer.book, self.book)

    def test_answer_representarion(self):
        answer = Answer.objects.create(choice=self.choice_1, user=self.user)
        self.assertEqual(str(answer), answer.choice.text)

    def test_answer_length(self):
        qtd_answers = 2
        for i in range(qtd_answers):
            answer = Answer.objects.create(choice=self.choice_1,
                                           user=self.user)

        self.assertEqual(len(answer), qtd_answers)


class PlayerTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='samuel',
                                        password='123456')
        self.player = Player.objects.create(user=user)
        book = Book.objects.create(title='Genealogia da Moral',
                                   author='Nietzsche',
                                   description='Uma descrição',
                                   user=user)
        self.question = Question.objects.create(book=book,
                                                user=user,
                                                text='Uma pergunta')
        choice_1 = Choice.objects.create(question=self.question,
                                         correct=True,
                                         text='Uma possível resposta')
        Choice.objects.create(question=self.question, correct=False,
                              text='Outra resposta')
        self.answer = Answer.objects.create(choice=choice_1,
                                            user=user)

    def test_add_point_to_player(self):
        qtd_choices_created_in_setUp = 2
        expected_point_value = qtd_choices_created_in_setUp * CHOICE_VALUE

        self.player.add_point(self.question, self.answer)
        point = self.player.points.get(player=self.player)
        self.assertEqual(point.value, expected_point_value)


class HomeViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='samuel', password='123456')
        self.client.login(username='samuel', password='123456')

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
        self.client.login(username='samuel', password='123456')

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
        self.choice = Choice.objects.create(question=self.question,
                                            correct=False,
                                            text='Uma possível resposta')
        self.client.login(username='samuel', password='123456')

    def test_get(self):
        response = self.client.get(f'/questions/play/{self.question.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/play.html')

    def test_post(self):
        payload = {'choice': [f'{self.choice.id}']}
        response = self.client.post(f'/questions/play/{self.question.id}',
                                    payload)
        self.assertRedirects(response, '/check_answer/1')


class MockAdminRequest:
    pass


class AdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='samuel',
                                             password='123456')
        self.site = AdminSite()
        self.mock_request = MockAdminRequest
        self.mock_request.user = self.user

    def test_admin_save_model_using_a_book(self):
        book = Book(title='teste', author='teste', description='teste',
                    user=self.user)
        book_admin = BookAdmin(book, self.site)
        book_admin.save_model(request=self.mock_request, obj=book_admin.model)
        self.assertIsNotNone(Book.objects.get(id=book.id))


class TestGameConfig(TestCase):
    def test_game_config_name(self):
        self.assertEqual(GameConfig.name, 'game')
