from django import forms
from django.contrib.auth.forms import AuthenticationForm
from mdeditor.fields import MDTextFormField
from django.http import HttpResponse
from solu_t.models import CustomUser
from django.core.mail import BadHeaderError, send_mail


class NoticePostForm(forms.Form):
    choice_base = forms.ChoiceField(label='通知拠点', choices=(
        ('青梅', '青梅'),
        ('坂戸', '坂戸'),
        ('相模原', '相模原')
    ),
                                    initial='',
                                    required=True,
                                    widget=forms.Select())
    choice_shift = forms.ChoiceField(label='通知時間帯', choices=(
        ('全体', '全体'),
        ('日勤', '日勤'),
        ('夜勤', '夜勤'),
    ),
                                     initial='',
                                     required=True,
                                     widget=forms.Select())
    choice_important = forms.ChoiceField(label='重要度', choices=(
        ('低', '低'),
        ('重要', '重要'),
    ),
                                         initial='',
                                         required=True,
                                         widget=forms.Select())
    title = forms.CharField(max_length=200, label='お知らせタイトル')
    content = forms.CharField(label='本文', widget=forms.Textarea(attrs={
        'placeholder': 'お知らせの内容をご記入ください',
    }),
                              required=True)
    choice_tag = forms.ChoiceField(label='タグ', choices=(
        ('追加出勤', '追加出勤'),
        ('協力休暇', '協力休暇'),
        ('追加出勤 + 協力休暇', '追加出勤 + 協力休暇'),
        ('その他', 'その他')
    ), required=False)


class SuperUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['placeholder'] = 'password'


class CustomContactForm(forms.Form):
    to = forms.ModelChoiceField(queryset=CustomUser.objects.order_by('-id'), to_field_name='email')
    kind_contact = forms.ChoiceField(label='お問い合わせの種類', choices=(
        ('', ''),
        ('休暇希望に関して', '休暇希望に関して'),
        ('書類に関して', '書類に関して'),
        ('現場に関して', '現場に関して'),
        ('その他に関して', 'その他に関して'),
    ),
                                     required=True,
                                     widget=forms.Select()
                                     )
    message = forms.CharField(label='内容', required=True, widget=forms.Textarea(attrs={
        'placeholder': 'お問い合わせの内容をご記入ください'
    }))

    # def send_email(self):
    #     name = self.cleaned_data['name']
    #     email = self.cleaned_data['email']
    #     message = self.cleaned_data['message']
    #     kind_contact = self.cleaned_data['kind_contact']
    #     base = self.cleaned_data['base']
    #     subject = '{base}所属： {name} 様より {kind_contact} のお問い合わせがありました'.format(base=base, name=name,
    #                                                                          kind_contact=kind_contact)
    #     from_sender = '{name} <{email}>'.format(name=name, email=email)
    #     message = 'お問い合わせ内容：{kind_contact}\n{message}\n\nhttps://solu-t.herokuapp.com/accounts/login/'.format(
    #         kind_contact=kind_contact, message=message)
    #
    #     recipient_list = 'kojimakai5335@gmail.com'
    #
    #     try:
    #         send_mail(subject, message, from_sender, recipient_list)
    #     except BadHeaderError:
    #         return HttpResponse('無効なヘッダが検出されました')
