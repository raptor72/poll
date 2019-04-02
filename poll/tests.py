from django.test import TestCase, Client
from .models import Poll, Question, Choice
from django.utils import timezone

from django.shortcuts import reverse
from django.contrib.auth.models import User, AnonymousUser


class PollTest(TestCase):
    def create_poll(self, title='test poll', slug='test_poll_url', comment='test comment', is_public=True):
        return Poll.objects.create(title=title,
                                   slug=slug,
                                   comment=comment,
                                   date_create=timezone.now(),
                                   is_public=is_public)
   
    def create_questions(self):
        qdict = ({'poll_id': 1, 'text': 'test question1', 'order': 0, 'answer': ''},
                 {'poll_id': 1, 'text': 'test question2', 'order': 0, 'answer': ''})

        for i in qdict:
            q = Question.objects.create(poll_id = i['poll_id'],
                                        text = i['text'],
                                        order = i['order'],
                                        answer = i['answer'])
        return q

    def create_choices(self):
        cdict = ({'question_id': 1, 'text': 'choice 1 for question 1', 'order': 0},
                 {'question_id': 1, 'text': 'choice 2 for question 1', 'order': 0},
                 {'question_id': 2, 'text': 'choice 1 for question 2', 'order': 0},
                 {'question_id': 2, 'text': 'choice 2 for question 2', 'order': 0})

        for i in cdict:
            c = Choice.objects.create(question_id = i['question_id'],
                                      text = i['text'],
                                      order = i['order'])
        return c

    def create_user(self, username = 'autotestuser', password = '123'):
        return User.objects.create_user(username =  username, password = password)

    def test_poll_creation(self):
        p = self.create_poll()
        self.assertTrue(isinstance(p, Poll))
        self.assertEqual(p.__str__(), p.title)

    def test_question_creation(self):
        q = self.create_questions()
        print("Question.id:", q.id)
        print("Question type:", type(q))
        self.assertTrue(isinstance(q, Question))

    def test_choice_creation(self):
        c = self.create_choices()
        self.assertTrue(isinstance(c, Choice))

    def test_polls_list_view(self):
        p = self.create_poll()
        url = reverse('polls_list_url')
        resp = self.client.get(url)
#        print(type(resp.content))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(p.title, str(resp.content))

    def test_poll_detail_unauthenticated(self):
        p = self.create_poll()
        url = reverse('poll_detail_url', args=[p.slug])
        resp = self.client.get(url)
        self.assertEqual(url, p.get_absolute_url())
        self.assertEqual(resp.status_code, 302)
        assert 'login' in resp.url

    def test_poll_detail_authenticated(self):
        p = self.create_poll()
        q = self.create_questions()
        c = self.create_choices()
        user = self.create_user()
        url = reverse('poll_detail_url', args=[p.slug])
        client = Client()
        client.login(username='autotestuser', password='123')
        request = client.get(url)
        print("request.content:", request.content)
#        self.assertEqual(url, p.get_absolute_url())
        self.assertEqual(request.status_code, 200)

    def test_poll_not_full_vote(self):
        p = self.create_poll()
        q = self.create_questions()
        c = self.create_choices()
        user = self.create_user()
        url = reverse('poll_detail_url', args=[p.slug])
        client = Client()
        client.login(username='autotestuser', password='123')
        request = client.post(url, {'choice - 1' : '1'})
#        print("request.content:", request.items, request.request)
        self.assertEqual(request.status_code, 302)

