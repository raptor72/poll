# Generated by Django 2.1.7 on 2019-03-14 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0008_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
