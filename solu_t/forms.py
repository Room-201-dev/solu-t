from django.conf import settings
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from mdeditor.fields import MDTextFormField

CustomUser = get_user_model()


def return_recipient_list(base):
    if base == '青梅':
        return ['tyo4@towa-cast.net']
    if base == '坂戸':
        return ['tyo6@towa-cast.net']
    if base == '相模原':
        return ['tyo8@towa-cast.net']


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'last_name', 'first_name', 'email', 'login_id', 'base', 'shift', 'assignment',
            'employee_number')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['placeholder'] = 'password'


class SorryForm(forms.Form):
    base = forms.CharField(label='拠点', max_length=10)
    choice_kind = forms.ChoiceField(label='申請内容', choices=(
        ('欠勤', '欠勤'),
        ('遅刻', '遅刻'),
    ))
    name = forms.CharField(max_length=100)
    employee_number = forms.CharField(max_length=50)
    reason = forms.ChoiceField(label='理由', choices=(
        ('体調不良', '体調不良'),
        ('家庭都合', '家庭都合'),
        ('寝坊', '寝坊'),
        ('私用', '私用'),
        ('天災', '天災'),
    ))
    reason_detail = forms.ChoiceField(label='理由詳細', choices=(
        ('腹痛', '腹痛'),
        ('風邪', '風邪'),
        ('倦怠感', '倦怠感'),
        ('吐き気', '吐き気'),
        ('腹痛★', '生理痛'),
        ('熱', '熱'),
        ('足痛', '足痛'),
        ('関節痛', '関節痛'),
        ('眩暈', '眩暈'),
        ('胃痛', '胃痛'),
        ('怪我', '怪我'),
        ('首痛', '首痛'),
        ('歯痛', '歯痛'),
        ('アレルギー', 'アレルギー'),
        ('目痛', '目痛'),
        ('咳', '咳'),
        ('肩痛', '肩痛'),
        ('腕痛', '腕痛'),
        ('背痛', '背痛'),
        ('胸痛', '胸痛'),
        ('耳痛', '耳痛'),
        ('蕁麻疹', '蕁麻疹'),
        ('リウマチ', 'リウマチ'),
        ('筋肉痛', '筋肉痛'),
        ('電車遅延', '電車遅延'),
        ('電車乗り遅れ', '電車遅延'),
        ('天災', '天災'),
        ('私用', '私用'),
        ('寝坊', '寝坊'),
        ('バッチ忘れ', 'バッチ忘れ'),
        ('現場不満', '現場不満'),
        ('学業都合', '学業都合'),
        ('バッチ紛失', 'バッチ紛失'),
        ('通院', '通院'),
        ('家族看病', '家族看病'),
        ('忌引', '忌引'),
    ))
    next_date = forms.ChoiceField(label='翌日', choices=(
        ('公休', '公休日'),
        ('OK', 'OK'),
        ('休希', '休暇希望'),
        ('リ休', 'リフレッシュ休暇'),
    ))
    assignment = forms.CharField(max_length=50)
    work_time = forms.ChoiceField(label='出勤予定時間※遅刻の場合は到着時間', choices=(
        ('8:00', '8:00'),
        ('8:30', '8:30'),
        ('9:00', '9:00'),
        ('9:30', '9:30'),
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('20:00', '20:00'),
        ('20:30', '20:30'),
        ('21:00', '21:00'),
        ('21:30', '21:30'),
        ('22:00', '22:00'),
        ('22:30', '22:30'),
        ('23:00', '23:00'),
    ), required=False)
    exit_time = forms.ChoiceField(label='退勤予定時刻', choices=(
        ('6:00', '6:00'),
        ('7:00', '7:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
    ), required=False)
    behind_work = forms.ChoiceField(label='本来の出勤時刻※遅刻の方のみ', choices=(
        ('', ''),
        ('8:00', '8:00'),
        ('8:30', '8:30'),
        ('9:00', '9:00'),
        ('9:30', '9:30'),
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('20:00', '20:00'),
        ('20:30', '20:30'),
        ('21:00', '21:00'),
        ('21:30', '21:30'),
        ('22:00', '22:00'),
        ('22:30', '22:30'),
        ('23:00', '23:00'),
    ), required=False)
    behind_exit = forms.ChoiceField(label='退勤予定時刻', choices=(
        ('', ''),
        ('6:00', '6:00'),
        ('7:00', '7:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
    ), required=False)
    temperature = forms.CharField(label='体温', max_length=50)
    login_id = forms.CharField(label='ログインID', max_length=50)
    lost_time = forms.IntegerField(label='欠損時間', min_value=1, max_value=10, required=False)

    def send_email(self):
        assignment = self.cleaned_data['assignment']
        base = self.cleaned_data['base']
        choice_kind = self.cleaned_data['choice_kind']
        name = self.cleaned_data['name']
        employee_number = self.cleaned_data['employee_number']
        reason = self.cleaned_data['reason']
        reason_detail = self.cleaned_data['reason_detail']
        next_date = self.cleaned_data['next_date']

        if self.cleaned_data['work_time'] is None:
            work_time = ''
        else:
            work_time = self.cleaned_data['work_time']

        if self.cleaned_data['exit_time'] is None:
            exit_time = ''
        else:
            exit_time = self.cleaned_data['exit_time']

        if self.cleaned_data['behind_work'] is None:
            behind_work = ''
        else:
            behind_work = self.cleaned_data['behind_work']

        if self.cleaned_data['behind_exit'] is None:
            behind_exit = ''
        else:
            behind_exit = self.cleaned_data['behind_exit']

        temperature = self.cleaned_data['temperature']
        login_id = self.cleaned_data['login_id']

        if self.cleaned_data['lost_time'] is None:
            lost_time = ''
        else:
            lost_time = self.cleaned_data['lost_time']

        subject = '{base}所属：{name} 様より {choice_kind}連絡 が届いております'.format(base=base, name=name.replace('　', ''),
                                                                        choice_kind=choice_kind)
        content = ''

        recipient_list = return_recipient_list(base)

        try:
            if base == '青梅':
                send_mail(subject, content, 'solu-t@staff', recipient_list,
                          html_message='<table border="1"><tr><th>東和キャスト</th><th>{choice_kind}</th><th>{employee_number}</th><th>{name}</th><th>{reason}</th><th>{reason_detail}</th><th>{next_date}</th><th>{assignment}</th><th>{work_time}</th><th>{exit_time}</th><th>{behind_work}</th><th>{behind_exit}</th><th></th><th>{temperature}℃</th></tr></table>'.format(
                              assignment=assignment,
                              name=name.replace('　', ''),
                              employee_number=employee_number,
                              choice_kind=choice_kind,
                              reason=reason,
                              reason_detail=reason_detail,
                              next_date=next_date,
                              work_time=work_time,
                              exit_time=exit_time,
                              behind_work=behind_work,
                              behind_exit=behind_exit,
                              temperature=temperature, ))
            elif base == '坂戸':
                send_mail(subject, content, 'solu-t@staff', recipient_list,
                          html_message='<table border="1"><tr><th>{assignment}</th><th>RG</th><th>東和キャスト</th><th>{login_id}</th><th>{name}</th><th>{choice_kind}</th><th>{lost_time}h</th><th>本人</th><th>{next_date}</th><th>{reason_detail}</th></tr></table>'.format(
                              assignment=assignment.replace('bound', '').upper(),
                              name=name.replace('　', ''),
                              login_id=login_id,
                              lost_time=lost_time,
                              choice_kind=choice_kind,
                              next_date=next_date,
                              reason=reason,
                              reason_detail=reason_detail,
                              temperature=temperature, ))
            elif base == '相模原':
                send_mail(subject, content, 'solu-t@staff', recipient_list,
                          html_message='<table border="1"><tr><th>{assignment}</th><th>東和キャスト</th><th>{login_id}</th><th>{name}</th><th>{choice_kind}</th><th>{lost_time}h</th><th>本人</th><th>{next_date}</th><th>{reason_detail}</th></tr></table>'.format(
                              assignment=assignment.replace('bound', '').upper(),
                              name=name.replace('　', ''),
                              login_id=login_id,
                              lost_time=lost_time,
                              choice_kind=choice_kind,
                              next_date=next_date,
                              reason=reason,
                              reason_detail=reason_detail,
                              temperature=temperature, ))

        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')


class ApplyBaseForm(forms.Form):
    base = forms.CharField(label='拠点', max_length=10)
    assignment = forms.CharField(label='大工程', max_length=50)
    name = forms.CharField(label='名前', max_length=100)
    choice_kind = forms.ChoiceField(label='申請内容', choices=(
        ('休暇希望', 'お休み希望'),
        ('振替', '振替希望'),
    ),
                                    initial='休暇 希望',
                                    required=True,
                                    widget=forms.Select())
    date = forms.DateField(label='休暇希望日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    work_date = forms.DateField(label='振替休暇日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    holiday_date = forms.DateField(label='振替出勤日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    work_time = forms.ChoiceField(label='勤務時間', choices=(
        ('', ''),
        ('β19', '8-19時'),
        ('B17', '8-17時'),
        ('C18', '9-18時'),
        ('ν31', '20-翌7時'),
        ('O30', '21-翌6時')
    ),
                                  initial='',
                                  required=False,
                                  widget=forms.Select())
    login_id = forms.CharField(label='ログインID', max_length=50)
    email = forms.EmailField(label='メールアドレス')
    paid_leave = forms.ChoiceField(label='有給', choices=(
        ('', ''),
        ('有給', '有給'),
    ),
                                   initial='',
                                   required=False,
                                   widget=forms.Select())

    def send_email(self):
        assignment = self.cleaned_data['assignment']
        name = self.cleaned_data['name']

        if self.cleaned_data['date'] is None:
            date = ' '
        else:
            date = self.cleaned_data['date'].strftime('%Y/%m/%d')

        login_id = self.cleaned_data['login_id']
        choice_kind = self.cleaned_data['choice_kind']
        base = self.cleaned_data['base']

        if self.cleaned_data['work_date'] is None:
            work_date = ' '
        else:
            work_date = self.cleaned_data['work_date'].strftime('%Y/%m/%d')

        if self.cleaned_data['holiday_date'] is None:
            holiday_date = ' '
        else:
            holiday_date = self.cleaned_data['holiday_date'].strftime('%Y/%m/%d')

        work_time = self.cleaned_data['work_time']

        if self.cleaned_data['paid_leave'] == '':
            paid_leave = ''
        else:
            paid_leave = '<有給>'

        subject = '{base}所属：{name} 様より{choice_kind} {paid_leave} が届いております'.format(base=base,
                                                                                  name=name.replace('　', ''),
                                                                                  choice_kind=choice_kind.replace(' ',
                                                                                                                  ''),
                                                                                  paid_leave=paid_leave)
        content = '{name}{login_id}{choice_kind}{date}{work_date}{holiday_date}{work_time}'.format(
            assignment=assignment,
            name=name,
            login_id=login_id,
            choice_kind=choice_kind,
            date=date,
            work_date=work_date,
            holiday_date=holiday_date,
            work_time=work_time)

        recipient_list = return_recipient_list(base)

        try:
            send_mail(subject, content, 'solu-t@staff', recipient_list,
                      html_message='<table border="1"><tr><th>東和キャスト</th><th>{assignment}</th><th>{name}</th><th>{login_id}</th><th></th><th>{choice_kind}</th><th>{date}</th><th>{holiday_date}</th><th>{work_date}</th><th>{work_time}</th></tr></table>\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
                          assignment=assignment,
                          name=name,
                          login_id=login_id,
                          choice_kind=choice_kind,
                          date=date, work_date=work_date,
                          holiday_date=holiday_date, work_time=work_time))
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')


class ApplyCustomizeForm(forms.Form):
    base = forms.CharField(label='拠点', max_length=10)
    assignment = forms.CharField(label='大工程', max_length=50)
    name = forms.CharField(label='名前', max_length=100)
    choice_kind = forms.ChoiceField(label='申請内容', choices=(
        ('休暇 希望', 'お休み希望'),
        ('振替 希望', '振替希望'),
    ),
                                    initial='休暇 希望',
                                    required=True,
                                    widget=forms.Select())
    date = forms.DateField(label='休暇希望日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    work_date = forms.DateField(label='振替休暇日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    holiday_date = forms.DateField(label='振替出勤日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    work_time = forms.ChoiceField(label='勤務時間', choices=(
        ('', ''),
        ('β19（8-19）', '8-19時'),
        ('B17（8-17）', '8-17時'),
        ('D19（10-19）', '10-19時'),
        ('M30（19-30）', '19-翌6時'),
        ('O30（21-30）', '21-翌6時')
    ),
                                  initial='',
                                  required=False,
                                  widget=forms.Select())
    login_id = forms.CharField(label='ログインID', max_length=50)
    email = forms.EmailField(label='メールアドレス')
    paid_leave = forms.ChoiceField(label='有給', choices=(
        ('', ''),
        ('有給', '有給'),
    ),
                                   initial='',
                                   required=False,
                                   widget=forms.Select())

    def send_email(self):
        assignment = self.cleaned_data['assignment']
        name = self.cleaned_data['name']

        if self.cleaned_data['date'] is None:
            date = ' '
        else:
            date = self.cleaned_data['date'].strftime('%Y/%m/%d')

        login_id = self.cleaned_data['login_id']
        choice_kind = self.cleaned_data['choice_kind']
        base = self.cleaned_data['base']

        if self.cleaned_data['work_date'] is None:
            work_date = ' '
        else:
            work_date = self.cleaned_data['work_date'].strftime('%Y/%m/%d')

        if self.cleaned_data['holiday_date'] is None:
            holiday_date = ' '
        else:
            holiday_date = self.cleaned_data['holiday_date'].strftime('%Y/%m/%d')

        work_time = self.cleaned_data['work_time']

        if self.cleaned_data['paid_leave'] == '':
            paid_leave = ''
        else:
            paid_leave = '<有給>'

        subject = '{name} 様より{choice_kind} {paid_leave} が届いております'.format(name=name.replace('　', ''),
                                                                         choice_kind=choice_kind.replace(' ', ''),
                                                                         paid_leave=paid_leave)
        content = '{name}{login_id}{choice_kind}{date}{work_date}{holiday_date}{work_time}'.format(
            assignment=assignment,
            name=name,
            login_id=login_id,
            choice_kind=choice_kind,
            date=date,
            work_date=work_date,
            holiday_date=holiday_date,
            work_time=work_time)

        recipient_list = return_recipient_list(base)

        try:
            send_mail(subject, content, 'solu-t@staff', recipient_list,
                      html_message='<table border="1"><tr><th>東和キャスト</th><th>{assignment}</th><th>{name}</th><th>{login_id}</th><th></th><th>{choice_kind}</th><th>{date}</th><th>{holiday_date}</th><th>{work_date}</th><th>{work_time}</th></tr></table>\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
                          assignment=assignment,
                          name=name,
                          login_id=login_id,
                          choice_kind=choice_kind,
                          date=date, work_date=work_date,
                          holiday_date=holiday_date, work_time=work_time))
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')


class BasePlusWorkForm(forms.Form):
    base = forms.CharField(label='所属拠点', max_length=10)
    assignment = forms.CharField(label='大工程', max_length=50)
    name = forms.CharField(label='名前', max_length=100)
    plus_work = forms.DateField(label='追加出勤日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    work_time = forms.ChoiceField(label='勤務時間', choices=(
        ('', ''),
        ('β19', '8-19時'),
        ('B17', '8-17時'),
        ('C18', '9-18時'),
        ('ν31', '20-翌7時'),
        ('O30', '21-翌6時')
    ),
                                  initial='',
                                  required=True,
                                  widget=forms.Select())
    login_id = forms.CharField(label='ログインID', max_length=50)
    email = forms.EmailField(label='メールアドレス')
    remarks_area = forms.CharField(label='1時間のみご協力いただける方はこちら', max_length=100, required=False)

    def send_email(self):
        base = self.cleaned_data['base']
        assignment = self.cleaned_data['assignment']
        name = self.cleaned_data['name']
        login_id = self.cleaned_data['login_id']

        if self.cleaned_data['plus_work'] is None:
            plus_work = ' '
        else:
            plus_work = self.cleaned_data['plus_work'].strftime('%Y/%m/%d')

        work_time = self.cleaned_data['work_time']
        subject = '{name} 様より 追加出勤希望 が届いております'.format(name=name.replace('　', ''))
        content = '{name}{login_id}{plus_work}{work_time}'.format(
            assignment=assignment,
            name=name,
            login_id=login_id,
            plus_work=plus_work,
            work_time=work_time)

        recipient_list = return_recipient_list(base)

        try:
            send_mail(subject, content, 'solu-t@staff', recipient_list,
                      html_message='<table border="1"><tr><th>東和キャスト</th><th>{assignment}</th><th>{name}</th><th>{login_id}</th><th></th><th>休日出勤</th><th></th><th></th><th></th><th></th><th>{plus_work}</th><th></th><th>{work_time}</th><th></th><th></th><th></th></tr></table>\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
                          assignment=assignment,
                          name=name,
                          login_id=login_id,
                          plus_work=plus_work,
                          work_time=work_time, ))
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')


class CustomPlusWorkForm(forms.Form):
    base = forms.CharField(label='所属拠点', max_length=10)
    assignment = forms.CharField(label='大工程', max_length=50)
    name = forms.CharField(label='名前', max_length=100)
    plus_work = forms.DateField(label='追加出勤日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }))
    work_time = forms.ChoiceField(label='勤務時間', choices=(
        ('', ''),
        ('β19（8-19）', '8-19時'),
        ('B17（8-17）', '8-17時'),
        ('D19（10-19）', '10-19時'),
        ('M30（19-30）', '19-翌6時'),
        ('O30（21-30）', '21-翌6時')
    ),
                                  initial='',
                                  required=True,
                                  widget=forms.Select())
    login_id = forms.CharField(label='ログインID', max_length=50)
    email = forms.EmailField(label='メールアドレス')

    def send_email(self):
        base = self.cleaned_data['base']
        assignment = self.cleaned_data['assignment']
        name = self.cleaned_data['name']
        login_id = self.cleaned_data['login_id']

        if self.cleaned_data['plus_work'] is None:
            plus_work = ' '
        else:
            plus_work = self.cleaned_data['plus_work'].strftime('%Y/%m/%d')

        work_time = self.cleaned_data['work_time']
        subject = '{name} 様より 追加出勤希望 が届いております'.format(name=name.replace('　', ''))
        content = '{name}{login_id}{plus_work}{work_time}'.format(
            assignment=assignment,
            name=name,
            login_id=login_id,
            plus_work=plus_work,
            work_time=work_time)

        recipient_list = return_recipient_list(base)

        try:
            send_mail(subject, content, 'solu-t@staff', recipient_list,
                      html_message='<table border="1"><tr><th>東和キャスト</th><th>{assignment}</th><th>{name}</th><th>{login_id}</th><th></th><th>休出 希望</th><th></th><th></th><th></th><th></th><th>{plus_work}</th><th>{work_time}</th><th></th><th></th><th></th></tr></table>\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
                          assignment=assignment,
                          name=name,
                          login_id=login_id,
                          plus_work=plus_work,
                          work_time=work_time, ))
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')


class BaseRefreshDayForm(forms.Form):
    base = forms.CharField(label='所属拠点', max_length=10)
    assignment = forms.CharField(label='大工程', max_length=50)
    name = forms.CharField(label='名前', max_length=100)
    choice_kind = forms.ChoiceField(label='勤務時間', choices=(
        ('リフレッシュ休暇', '協力休暇'),
        ('時短', '時短'),
    ),
                                    initial='リフレッシュ休暇',
                                    required=True,
                                    widget=forms.Select())
    refresh_date = forms.DateField(label='協力休暇日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    early_date = forms.DateField(label='時短協力日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    early_work = forms.ChoiceField(label='勤務時間', choices=(
        ('', ''),
        ('B17', '8-17時'),
        ('C16', '9-16時'),
        ('C18', '9-18時'),
        ('O30', '21-翌6時')
    ),
                                   initial='',
                                   required=False,
                                   widget=forms.Select())
    login_id = forms.CharField(label='ログインID', max_length=50)
    email = forms.EmailField(label='メールアドレス')

    def send_email(self):
        base = self.cleaned_data['base']
        assignment = self.cleaned_data['assignment']
        name = self.cleaned_data['name']
        login_id = self.cleaned_data['login_id']
        choice_kind = self.cleaned_data['choice_kind']

        if self.cleaned_data['refresh_date'] is None:
            refresh_date = ' '
        else:
            refresh_date = self.cleaned_data['refresh_date'].strftime('%Y/%m/%d')

        if self.cleaned_data['early_date'] is None:
            early_date = ' '
        else:
            early_date = self.cleaned_data['early_date'].strftime('%Y/%m/%d')

        early_work = self.cleaned_data['early_work']
        subject = '{name} 様より リフレッシュ休暇・時短希望 が届いております'.format(name=name.replace('　', ''),
                                                             choice_kind=choice_kind)
        content = '{assignment}{name}{login_id}{choice_kind}{early_date}{early_work}{refresh_date}'.format(
            assignment=assignment,
            name=name,
            login_id=login_id,
            choice_kind=choice_kind,
            early_date=early_date,
            early_work=early_work,
            refresh_date=refresh_date, )

        recipient_list = return_recipient_list(base)

        try:
            send_mail(subject, content, 'solu-t@staff', recipient_list,
                      html_message='<table border="1"><tr><th>東和キャスト</th><th>{assignment}</th><th>{name}</th><th>{login_id}</th><th></th><th>{choice_kind}</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th>{early_date}</th><th>{early_work}</th><th>{refresh_date}</th></tr></table>\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
                          assignment=assignment,
                          name=name,
                          login_id=login_id,
                          choice_kind=choice_kind,
                          refresh_date=refresh_date,
                          early_date=early_date,
                          early_work=early_work, ))
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')


class CustomRefreshDayForm(forms.Form):
    base = forms.CharField(label='所属拠点', max_length=10)
    assignment = forms.CharField(label='大工程', max_length=50)
    name = forms.CharField(label='名前', max_length=100)
    refresh_date = forms.DateField(label='協力休暇日', widget=DatePickerInput(format='%Y/%m/%d', options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
    }), required=False)
    login_id = forms.CharField(label='ログインID', max_length=50)
    email = forms.EmailField(label='メールアドレス')

    def send_email(self):
        assignment = self.cleaned_data['assignment']
        name = self.cleaned_data['name']
        login_id = self.cleaned_data['login_id']
        choice_kind = 'リフレッシュ休暇'
        base = self.cleaned_data['base']

        if self.cleaned_data['refresh_date'] is None:
            refresh_date = ' '
        else:
            refresh_date = self.cleaned_data['refresh_date'].strftime('%Y/%m/%d')

        subject = '{base}所属：{name} 様より リフレッシュ休暇希望 が届いております'.format(base=base, name=name.replace('　', ''))
        content = '{assignment}{name}{login_id}{choice_kind}{refresh_date}'.format(
            assignment=assignment,
            name=name,
            login_id=login_id,
            choice_kind=choice_kind,
            refresh_date=refresh_date, )

        recipient_list = return_recipient_list(base)

        try:
            send_mail(subject, content, 'solu-t@staff', recipient_list,
                      html_message='<table border="1"><tr><th>東和キャスト</th><th>{assignment}</th><th>{name}</th><th>{login_id}</th><th></th><th>{choice_kind}</th><th></th><th></th><th></th><th></th><th></th><th></th><th>{refresh_date}</th></tr></table>\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
                          assignment=assignment,
                          name=name,
                          login_id=login_id,
                          choice_kind=choice_kind,
                          refresh_date=refresh_date, ))
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')


class ContactForm(forms.Form):
    kind_contact = forms.ChoiceField(label='お問い合わせの種類', choices=(
        ('休暇希望に関して', '休暇希望に関して'),
        ('書類に関して', '書類に関して'),
        ('現場に関して', '現場に関して'),
        ('その他に関して', 'その他に関して'),
    ),
                                     required=True,
                                     widget=forms.Select()
                                     )
    name = forms.CharField(label='お名前', max_length=100, widget=forms.TextInput(attrs={
        'class': 'name_form',
        'placeholder': '山田 太郎',
    }))
    email = forms.EmailField(label='メールアドレス', widget=forms.EmailInput(attrs={
        'class': 'email_form',
    }))
    base = forms.CharField(max_length=10)
    message = forms.CharField(label='内容', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'お問い合わせの内容をご記入ください'
    }))

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        kind_contact = self.cleaned_data['kind_contact']
        base = self.cleaned_data['base']
        subject = '{base}所属： {name} 様より {kind_contact} のお問い合わせがありました'.format(base=base, name=name,
                                                                             kind_contact=kind_contact)
        from_sender = '{name} <{email}>'.format(name=name, email=email)
        message = 'お問い合わせ内容：{kind_contact}\n{message}\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
            kind_contact=kind_contact, message=message)

        recipient_list = return_recipient_list(base)

        try:
            send_mail(subject, message, from_sender, recipient_list)
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました')
