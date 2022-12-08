from django import forms
from django.contrib.auth.forms import AuthenticationForm
from mdeditor.fields import MDTextFormField


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
