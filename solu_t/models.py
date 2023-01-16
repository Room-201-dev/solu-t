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

    login_id = models.CharField('Login ID', max_length=50, unique=True)
    employee_number = models.CharField('社員番号', max_length=50, unique=True)
    assignment = models.CharField('大工程', max_length=10, choices=ASSIGNMENT_CHOICES)
    base = models.CharField('所属拠点', max_length=10, choices=BASE_CHOICE)
    shift = models.CharField('勤務シフト', max_length=5, choices=SHIFT_CHOICE)
    time = models.CharField('勤務時間', max_length=20, null=True, blank=True)
    day = models.CharField('曜日シフト', max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['login_id', 'employee_number', 'base', 'shift', 'assignment']

    def __str__(self):
        return f"{self.last_name} {self.first_name} <{self.email}>"


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
        return f"to.{self.base} > {self.title}"


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
        return f"{self.name} > {self.choice_kind}"


class ApplyData(models.Model):
    name = models.CharField('名前', max_length=100)
    choice_kind = models.CharField('申請内容', max_length=30)
    date = models.DateField('休暇日', blank=True, null=True)
    refresh_date = models.DateField('リフレッシュ休暇', blank=True, null=True)
    base = models.CharField('拠点', max_length=10)

    def __str__(self):
        return f"{self.name} > {self.choice_kind}"


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
        return f"{self.base}：{self.name}から{self.contact_kind}のお問い合わせ"


class ShiftDataModel(models.Model):
    user_id = models.CharField('UserID', max_length=1000, blank=True, null=True)
    assign = models.CharField('所属', max_length=10)
    name = models.CharField('名前', max_length=50)
    email = models.EmailField('メールアドレス', unique=True)
    choice = models.CharField('希望', max_length=10)
    current_day = models.CharField('現在の曜日シフト', max_length=50, blank=True, null=True)
    current_time = models.CharField('現在の勤務時間', max_length=50, blank=True, null=True)
    firstchoice_time = models.CharField('第一希望時間', max_length=50, blank=True, null=True)
    firstchoice_day = models.CharField('第一希望曜日', max_length=50, blank=True, null=True)
    secondchoice_time = models.CharField('第二希望時間', max_length=50, blank=True, null=True)
    secondchoice_day = models.CharField('第二希望曜日', max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.assign}：{self.name}"
