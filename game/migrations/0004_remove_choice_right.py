# Generated by Django 3.0 on 2020-05-31 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_question_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='right',
        ),
    ]