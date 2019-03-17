from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import User

class Poll(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    comment = models.TextField(blank=True, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('poll_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def user_can_vote(self, user):
        query_set = user.vote_set.all().filter(poll=self)
        if query_set.exists():
            return False
        return True

    def num_votes(self):
        s = set()
        for i in self.vote_set.all():
            s.add(i.user)
        return len(s)


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    order = models.IntegerField(default=0)
    answer = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return '{}'.format(self.text)

    class Meta:
        ordering = ['order']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def num_votes(self):
        return self.vote_set.count()

    def percent(self):
        if self.num_votes() == 0:
            return 0
        else:
            percent = round((self.num_votes() / Poll.num_votes(self.question.poll) * 100), 2)
            return percent

    class Meta:
        ordering = ['order']

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

