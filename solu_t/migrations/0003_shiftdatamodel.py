# Generated by Django 4.1.3 on 2023-01-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solu_t', '0002_delete_shiftdatamodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=1000, null=True, verbose_name='UserID')),
                ('assign', models.CharField(max_length=10, verbose_name='所属')),
                ('name', models.CharField(max_length=50, verbose_name='名前')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('choice', models.CharField(max_length=10, verbose_name='希望')),
                ('current_day', models.CharField(blank=True, max_length=50, null=True, verbose_name='現在の曜日シフト')),
                ('current_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='現在の勤務時間')),
                ('firstchoice_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='第一希望時間')),
                ('firstchoice_day', models.CharField(blank=True, max_length=50, null=True, verbose_name='第一希望曜日')),
                ('secondchoice_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='第二希望時間')),
                ('secondchoice_day', models.CharField(blank=True, max_length=50, null=True, verbose_name='第二希望曜日')),
            ],
        ),
    ]
