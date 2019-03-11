from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    comment = models.TextField(blank=True, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    questions = models.ManyToManyField('Question', blank=True, related_name='polls')

    def get_absolute_url(self):
        return reverse('poll_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)


class Question(models.Model):
    text = models.CharField(max_length=150)
    case = models.CharField(max_length=150, blank=True)
    answer = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return '{}'.format(self.text)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    text = models.CharField(max_length=150)
    is_answered = models.BooleanField(default=False)

#    def make_choise(self):
