# Generated by Django 4.1.3 on 2023-01-16 12:55

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('choice_kind', models.CharField(max_length=30, verbose_name='申請内容')),
                ('date', models.DateField(blank=True, null=True, verbose_name='休暇日')),
                ('refresh_date', models.DateField(blank=True, null=True, verbose_name='リフレッシュ休暇')),
                ('base', models.CharField(max_length=10, verbose_name='拠点')),
            ],
        ),
        migrations.CreateModel(
            name='ApplyList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=10, verbose_name='拠点')),
                ('assignment', models.CharField(max_length=50, verbose_name='大工程')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('login_id', models.CharField(max_length=50, verbose_name='ログインID')),
                ('choice_kind', models.CharField(max_length=30, verbose_name='申請内容')),
                ('date', models.DateField(blank=True, null=True, verbose_name='休暇申請日')),
                ('holiday_date', models.DateField(blank=True, null=True, verbose_name='振休')),
                ('work_date', models.DateField(blank=True, null=True, verbose_name='振出')),
                ('work_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='勤務時間')),
                ('plus_work', models.DateField(blank=True, max_length=30, null=True, verbose_name='休出日程')),
                ('overtime_date', models.DateField(blank=True, max_length=30, null=True, verbose_name='残業日')),
                ('overtime', models.CharField(blank=True, max_length=30, null=True, verbose_name='休出勤務時間')),
                ('early_date', models.DateField(blank=True, max_length=30, null=True, verbose_name='時短日程')),
                ('early_work', models.CharField(blank=True, max_length=50, null=True, verbose_name='勤務時間')),
                ('refresh_date', models.DateField(blank=True, max_length=30, null=True, verbose_name='リフレッシュ休暇')),
                ('email', models.EmailField(max_length=254, verbose_name='メールアドレス')),
                ('remarks_area', models.CharField(blank=True, max_length=100, null=True, verbose_name='備考欄')),
            ],
        ),
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('email', models.EmailField(max_length=254, verbose_name='メールアドレス')),
                ('base', models.CharField(choices=[('青梅', '青梅FC'), ('坂戸', '坂戸FC'), ('相模原', '相模原FC')], max_length=10, verbose_name='所属拠点')),
                ('contact_kind', models.CharField(max_length=50, verbose_name='お問い合わせの種類')),
                ('message', models.TextField(default='', verbose_name='お知らせ内容')),
                ('tag', models.CharField(max_length=20, null=True, verbose_name='タグ')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('important', models.CharField(choices=[('低', '低'), ('重要', '重要')], max_length=5, verbose_name='重要度')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='本文')),
                ('base', models.CharField(choices=[('青梅', '青梅FC'), ('坂戸', '坂戸FC'), ('相模原', '相模原FC')], max_length=10, verbose_name='所属拠点')),
                ('shift', models.CharField(choices=[('日勤', '日勤'), ('夜勤', '夜勤'), ('全体', '全体')], max_length=5, verbose_name='勤務シフト')),
                ('tag', models.CharField(blank=True, choices=[('追加出勤', '追加出勤'), ('協力休暇', '協力休暇'), ('追加出勤 + 協力休暇', '追加出勤 + 協力休暇'), ('その他', 'その他')], max_length=20, null=True, verbose_name='タグ')),
            ],
        ),
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
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('login_id', models.CharField(max_length=50, unique=True, verbose_name='Login ID')),
                ('employee_number', models.CharField(max_length=50, unique=True, verbose_name='社員番号')),
                ('assignment', models.CharField(choices=[('Outbound', 'OUT'), ('Inbound', 'IN')], max_length=10, verbose_name='大工程')),
                ('base', models.CharField(choices=[('青梅', '青梅FC'), ('坂戸', '坂戸FC'), ('相模原', '相模原FC')], max_length=10, verbose_name='所属拠点')),
                ('shift', models.CharField(choices=[('日勤', '日勤'), ('夜勤', '夜勤')], max_length=5, verbose_name='勤務シフト')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
