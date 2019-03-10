from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    comment = models.TextField(blank=True, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('poll_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

