from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    ASSIGNMENT_CHOICES = (
        ('Outbound', 'OUT'),
        ('Inbound', 'IN'),
    )
    BASE_CHOICE = (
        ('青梅', '青梅FC'),
        ('坂戸', '坂戸FC'),
        ('相模原', '相模原FC')
    )
    SHIFT_CHOICE = (
        ('日勤', '日勤'),
        ('夜勤', '夜勤')
    )

    login_id = models.CharField('Login ID', max_length=50)
    employee_number = models.CharField('社員番号', max_length=50)
    assignment = models.CharField('大工程', max_length=10, choices=ASSIGNMENT_CHOICES)
    base = models.CharField('所属拠点', max_length=10, choices=BASE_CHOICE)
    shift = models.CharField('勤務シフト', max_length=5, choices=SHIFT_CHOICE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['login_id', 'employee_number', 'base', 'shift', 'assignment']

    def __str__(self):
        return self.username


class Notice(models.Model):
    BASE_CHOICE = (
        ('青梅', '青梅FC'),
        ('坂戸', '坂戸FC'),
        ('相模原', '相模原FC')
    )
    SHIFT_CHOICE = (
        ('日勤', '日勤'),
        ('夜勤', '夜勤'),
        ('全体', '全体'),
    )
    IMPORTANT_CHOICE = (
        ('低', '低'),
        ('重要', '重要'),
    )
    TAG_CHOICE = (
        ('追加出勤', '追加出勤'),
        ('協力休暇', '協力休暇'),
        ('追加出勤 + 協力休暇', '追加出勤 + 協力休暇'),
        ('その他', 'その他')
    )

    important = models.CharField('重要度', max_length=5, choices=IMPORTANT_CHOICE)
    title = models.CharField('タイトル', max_length=200)
    content = models.TextField('本文')
    base = models.CharField('所属拠点', max_length=10, choices=BASE_CHOICE)
    shift = models.CharField('勤務シフト', max_length=5, choices=SHIFT_CHOICE)
    tag = models.CharField('タグ', max_length=20, choices=TAG_CHOICE, blank=True, null=True)

    def __str__(self):
        return self.title


class ApplyList(models.Model):
    base = models.CharField('拠点', max_length=10)
    assignment = models.CharField('大工程', max_length=50)
    name = models.CharField('名前', max_length=100)
    login_id = models.CharField('ログインID', max_length=50)
    choice_kind = models.CharField('申請内容', max_length=30)
    date = models.DateField('休暇申請日', blank=True, null=True)
    holiday_date = models.DateField('振休', blank=True, null=True)
    work_date = models.DateField('振出', blank=True, null=True)
    work_time = models.CharField('勤務時間', max_length=50, blank=True, null=True)
    plus_work = models.DateField('休出日程', max_length=30, blank=True, null=True)
    overtime_date = models.DateField('残業日', max_length=30, blank=True, null=True)
    overtime = models.CharField('休出勤務時間', max_length=30, blank=True, null=True)
    early_date = models.DateField('時短日程', max_length=30, blank=True, null=True)
    early_work = models.CharField('勤務時間', max_length=50, blank=True, null=True)
    refresh_date = models.DateField('リフレッシュ休暇', max_length=30, blank=True, null=True)
    email = models.EmailField('メールアドレス', unique=False)
    remarks_area = models.CharField('備考欄', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class ApplyData(models.Model):
    name = models.CharField('名前', max_length=100)
    choice_kind = models.CharField('申請内容', max_length=30)
    date = models.DateField('休暇日', blank=True, null=True)
    refresh_date = models.DateField('リフレッシュ休暇', blank=True, null=True)
    base = models.CharField('拠点', max_length=10)

    def __str__(self):
        return self.name


class ContactData(models.Model):
    BASE_CHOICE = (
        ('青梅', '青梅FC'),
        ('坂戸', '坂戸FC'),
        ('相模原', '相模原FC')
    )

    name = models.CharField('名前', max_length=100)
    email = models.EmailField('メールアドレス')
    base = models.CharField('所属拠点', max_length=10, choices=BASE_CHOICE)
    contact_kind = models.CharField('お問い合わせの種類', max_length=50)
    message = models.TextField(verbose_name='お知らせ内容', default='')
    tag = models.CharField('タグ', max_length=20, null=True)

    def __str__(self):
        return self.name
