from django.test import TestCase, Client
from .models import Poll, Question, Choice
from django.utils import timezone

from django.shortcuts import reverse
from django.contrib.auth.models import User


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

    def create_user(self, username = 'autotestuser', password = '123', is_superuser = False):
        return User.objects.create_user(username =  username, password = password, is_superuser = is_superuser)

    def test_poll_creation(self):
        p = self.create_poll()
        self.assertTrue(isinstance(p, Poll))
        self.assertEqual(p.__str__(), p.title)

    def test_question_creation(self):
        q = self.create_questions()
        self.assertTrue(isinstance(q, Question))
        self.assertEqual(q.__str__(), q.text)
 
    def test_choice_creation(self):
        c = self.create_choices()
        self.assertTrue(isinstance(c, Choice))
        self.assertEqual(c.__str__(), c.text)

    def test_redirect_poll(self):
        client = Client()
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 301)
        self.assertEqual('/poll/', resp.url)

    def test_polls_list_view(self):
        p = self.create_poll()
        url = reverse('polls_list_url')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(p.title, str(resp.content))

    def test_poll_detail_unauthenticated(self):
        p = self.create_poll()
        url = reverse('poll_detail_url', args=[p.slug])
        resp = self.client.get(url)
        self.assertEqual(url, p.get_absolute_url())
        self.assertEqual(resp.status_code, 302)
        self.assertIn('login', resp.url)

    def create_full_poll(self, path, args = None, postdata = None, superuser = False):
        p = self.create_poll()
        q = self.create_questions()
        c = self.create_choices()
        user = self.create_user(is_superuser = superuser)
        url = reverse(path, args = args)
        client = Client()
        client.login(username='autotestuser', password='123')
        rpost = client.post(url, postdata)
        rget = client.get(url)
        return rget, rpost

    def test_poll_result_not_superuser(self):
        request = self.create_full_poll('poll_result', args=['test_poll_url'])[0]
        self.assertEqual(request.status_code, 302)

    def test_poll_result_superuser(self):
        request = self.create_full_poll('poll_result', args=['test_poll_url'], superuser = True)[0]
        self.assertEqual(request.status_code, 200)

    def test_poll_detail_authenticated(self):
        request = self.create_full_poll('poll_detail_url', args=['test_poll_url'])[0]
        self.assertEqual(request.status_code, 200)
        self.assertIn('test_poll_url', request.request['PATH_INFO'])
        self.assertIn('question', str(request.content))

    def test_incomplete_vote(self):
        set =  self.create_full_poll('poll_detail_url' , args=['test_poll_url'], postdata = {'choice - 1' : '1'})
        rget = set[0]
        rpost = set[1]
        self.assertIn('You should choose one answer in each question', str(rget.content))
        self.assertIn('0 user voted', str(rget.content))
        self.assertEqual(rpost.status_code, 302)

    def test_complete_vote(self):
        set =  self.create_full_poll('poll_detail_url' , args=['test_poll_url'], postdata = {'choice - 1' : '1', 'choice - 2' : '3'})
        rget = set[0]
        rpost = set[1]
        for i in Choice.objects.all():
            self.assertLessEqual(i.percent(), 100)
        self.assertIn('1 user voted', str(rget.content))
        self.assertIn('value="Vote" disabled', str(rget.content))
        self.assertEqual(Poll.objects.first().user_can_vote(User.objects.first()), False)
        self.assertEqual(Poll.objects.first().num_votes(), 1)



