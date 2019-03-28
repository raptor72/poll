from django.test import TestCase
from .models import Poll
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

    def test_poll_creation(self):
        p = self.create_poll()
        self.assertTrue(isinstance(p, Poll))
        self.assertEqual(p.__str__(), p.title)

    def test_polls_list_view(self):
        p = self.create_poll()
        url = reverse('polls_list_url')
        resp = self.client.get(url)
#        print(resp.content)
#        print(type(resp.content))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(p.title, str(resp.content))

    def test_poll_detail_unauthenticated(self):
        p = self.create_poll()
        url = reverse('poll_detail_url', args=[p.slug])
        resp = self.client.get(url)
        self.assertEqual(url, p.get_absolute_url())
#        self.assertEqual(resp.status_code, 200)
        assert 'login' in resp.url

