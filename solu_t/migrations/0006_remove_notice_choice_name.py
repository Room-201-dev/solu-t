# Generated by Django 4.1.3 on 2022-11-30 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solu_t', '0005_notice_choice_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='choice_name',
        ),
    ]
