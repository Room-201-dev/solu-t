from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from allauth.account import views
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
import datetime
from dateutil.relativedelta import relativedelta

from .models import ApplyList, ApplyData, Notice, CustomUser, ContactData, ShiftDataModel

from .forms import SorryForm, ApplyBaseForm, ApplyCustomizeForm, SignUpForm, ContactForm, LoginForm, BasePlusWorkForm, \
    BaseRefreshDayForm, CustomPlusWorkForm, CustomRefreshDayForm, ShiftForm

from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'solu_t/sign_up.html'
    success_url = reverse_lazy('mypage')

    def get(self, request, *args, **kwargs):
        form = SignUpForm

        return render(request, 'solu_t/sign_up.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mypage')

        return render(request, 'solu_t/sign_up.html', {
            'form': form
        })


class LoginSolutView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        return render(request, 'solu_t/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = CustomUser.objects.get(username=username)
            login(request, user)
            return redirect('mypage')

        return render(request, 'solu_t/login.html', {'form': form})


class LogoutSolutView(LogoutView):
    template_name = 'solu_t/logout.html'


class ChangeScheduleView(LoginRequiredMixin, View):
    template_name = 'solu_t/change_schedule_from.html'
    success_url = reverse_lazy('mypage')

    def get(self, request, *args, **kwargs):
        user = request.user
        base_form = ApplyBaseForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'login_id': user.login_id,
            'assignment': user.assignment,
            'email': user.email,
            'base': user.base,
        })
        customize_form = ApplyCustomizeForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'login_id': user.login_id,
            'assignment': user.assignment,
            'email': user.email,
            'base': user.base,
        })

        return render(request, 'solu_t/change_schedule_from.html', {
            'base_form': base_form,
            'customize_form': customize_form,
        })

    def post(self, request, *args, **kwargs):
        base_form = ApplyBaseForm(request.POST or None)
        customize_form = ApplyCustomizeForm(request.POST or None)

        if base_form.is_valid():
            base_form.send_email()
            apply_list = ApplyList()
            apply_list.assignment = base_form.cleaned_data['assignment']
            apply_list.base = base_form.cleaned_data['base']
            apply_list.name = base_form.cleaned_data['name']
            apply_list.login_id = base_form.cleaned_data['login_id']
            apply_list.choice_kind = base_form.cleaned_data['choice_kind']
            apply_list.date = base_form.cleaned_data['date']
            apply_list.holiday_date = base_form.cleaned_data['holiday_date']
            apply_list.work_date = base_form.cleaned_data['work_date']
            apply_list.work_time = base_form.cleaned_data['work_time']
            apply_list.email = base_form.cleaned_data['email']
            apply_list.remarks_area = base_form.cleaned_data['paid_leave']
            apply_list.save()

            apply_data = ApplyData()
            if not base_form.cleaned_data['choice_kind'] == '振替':
                apply_data.base = base_form.cleaned_data['base']
                apply_data.name = base_form.cleaned_data['name']
                apply_data.choice_kind = base_form.cleaned_data['choice_kind']
                apply_data.date = base_form.cleaned_data['date']
                if base_form.cleaned_data['paid_leave']:
                    apply_data.choice_kind = base_form.cleaned_data['paid_leave']
                apply_data.save()

            context = {
                'name': apply_list.name.replace('　', ''),
                'kind': apply_list.choice_kind.replace(' ', ''),
                'holiday': apply_list.date,
                'makeup_holiday': apply_list.holiday_date,
                'makeup_workday': apply_list.work_date,
                'paid_leave': apply_list.remarks_area,
            }

            return render(request, 'solu_t/apply_complete.html', {
                'context': context
            })

        if customize_form.is_valid():
            customize_form.send_email()
            apply_list = ApplyList()
            apply_list.base = customize_form.cleaned_data['base']
            apply_list.assignment = customize_form.cleaned_data['assignment']
            apply_list.name = customize_form.cleaned_data['name']
            apply_list.login_id = customize_form.cleaned_data['login_id']
            apply_list.choice_kind = customize_form.cleaned_data['choice_kind']
            apply_list.date = customize_form.cleaned_data['date']
            apply_list.holiday_date = customize_form.cleaned_data['holiday_date']
            apply_list.work_date = customize_form.cleaned_data['work_date']
            apply_list.work_time = customize_form.cleaned_data['work_time']
            apply_list.email = customize_form.cleaned_data['email']
            apply_list.remarks_area = base_form.cleaned_data['paid_leave']
            apply_list.save()

            apply_data = ApplyData()
            if not customize_form.cleaned_data['choice_kind'] == '振替 希望':
                apply_data.base = customize_form.cleaned_data['base']
                apply_data.name = customize_form.cleaned_data['name']
                apply_data.choice_kind = customize_form.cleaned_data['choice_kind']
                apply_data.date = customize_form.cleaned_data['date']
                if customize_form.cleaned_data['paid_leave']:
                    apply_data.choice_kind = customize_form.cleaned_data['paid_leave']
                apply_data.save()

            context = {
                'name': apply_list.name.replace('　', ''),
                'kind': apply_list.choice_kind.replace(' ', ''),
                'holiday': apply_list.date,
                'makeup_holiday': apply_list.holiday_date,
                'makeup_workday': apply_list.work_date,
                'paid_leave': apply_list.remarks_area,
            }

            return render(request, 'solu_t/apply_complete.html', {
                'context': context
            })

        else:
            return HttpResponse('無効なヘッダが検出されました')


class SorryFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = SorryForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'login_id': user.login_id,
            'employee_number': user.employee_number,
            'assignment': user.assignment,
            'base': user.base,
        })

        return render(request, 'solu_t/sorry_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        form = SorryForm(request.POST or None)

        if form.is_valid():
            form.send_email()
            context = {
                'name': user.last_name
            }

            return render(request, 'solu_t/sorry...complete.html', context={
                'context': context
            })

        return render(request, 'solu_t/sorry_form.html', form)


class CoOneDayView(LoginRequiredMixin, View):
    template_name = 'solu_t/co_oneday_form.html'
    success_url = reverse_lazy('mypage')

    def get(self, request, *args, **kwargs):
        user = request.user
        base_form = BaseRefreshDayForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'login_id': user.login_id,
            'assignment': user.assignment,
            'email': user.email,
            'base': user.base,
        })
        customize_form = CustomRefreshDayForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'login_id': user.login_id,
            'assignment': user.assignment,
            'email': user.email,
            'base': user.base,
        })

        return render(request, 'solu_t/co_oneday_form.html', {
            'base_form': base_form,
            'customize_form': customize_form,
        })

    def post(self, request, *args, **kwargs):
        base_form = BaseRefreshDayForm(request.POST or None)
        customize_form = CustomRefreshDayForm(request.POST or None)

        if base_form.is_valid():
            base_form.send_email()
            apply_list = ApplyList()
            apply_list.assignment = base_form.cleaned_data['assignment']
            apply_list.base = base_form.cleaned_data['base']
            apply_list.name = base_form.cleaned_data['name']
            apply_list.login_id = base_form.cleaned_data['login_id']
            apply_list.choice_kind = base_form.cleaned_data['choice_kind']
            apply_list.refresh_date = base_form.cleaned_data['refresh_date']
            apply_list.early_date = base_form.cleaned_data['early_date']
            apply_list.early_work = base_form.cleaned_data['early_work']
            apply_list.email = base_form.cleaned_data['email']
            apply_list.save()

            apply_data = ApplyData()
            if not base_form.cleaned_data['refresh_date'] is None:
                apply_data.base = base_form.cleaned_data['base']
                apply_data.name = base_form.cleaned_data['name']
                apply_data.choice_kind = 'リフレッシュ休暇'
                apply_data.refresh_date = base_form.cleaned_data['refresh_date']
                apply_data.save()

            context = {
                'name': apply_list.name.replace('　', ''),
                'kind': apply_list.choice_kind.replace(' ', ''),
                'lh_adjust': apply_list.refresh_date,
            }

            return render(request, 'solu_t/lh_adjust_complete.html', {
                'context': context
            })

        if customize_form.is_valid():
            customize_form.send_email()
            apply_list = ApplyList()
            apply_list.base = customize_form.cleaned_data['base']
            apply_list.assignment = customize_form.cleaned_data['assignment']
            apply_list.name = customize_form.cleaned_data['name']
            apply_list.login_id = customize_form.cleaned_data['login_id']
            apply_list.choice_kind = 'リフレッシュ休暇'
            apply_list.refresh_date = customize_form.cleaned_data['refresh_date']
            apply_list.email = customize_form.cleaned_data['email']
            apply_list.save()

            apply_data = ApplyData()
            apply_data.base = customize_form.cleaned_data['base']
            apply_data.name = customize_form.cleaned_data['name']
            apply_data.choice_kind = 'リフレッシュ休暇'
            apply_data.refresh_date = customize_form.cleaned_data['refresh_date']
            apply_data.save()

            context = {
                'name': apply_list.name.replace('　', ''),
                'kind': apply_list.choice_kind.replace(' ', ''),
                'lh_adjust': apply_list.refresh_date,
            }

            return render(request, 'solu_t/lh_adjust_complete.html', {
                'context': context
            })

        else:
            return HttpResponse('無効なヘッダが検出されました')


class PlusWorkView(LoginRequiredMixin, View):
    template_name = 'solu_t/plus_work_form.html'
    success_url = reverse_lazy('mypage')

    def get(self, request, *args, **kwargs):
        user = request.user
        base_form = BasePlusWorkForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'login_id': user.login_id,
            'assignment': user.assignment,
            'email': user.email,
            'base': user.base,
        })
        customize_form = CustomPlusWorkForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'login_id': user.login_id,
            'assignment': user.assignment,
            'email': user.email,
            'base': user.base,
        })

        return render(request, 'solu_t/plus_work_form.html', {
            'base_form': base_form,
            'customize_form': customize_form,
        })

    def post(self, request, *args, **kwargs):
        base_form = BasePlusWorkForm(request.POST or None)
        customize_form = CustomPlusWorkForm(request.POST or None)

        if base_form.is_valid():
            base_form.send_email()
            apply_list = ApplyList()
            apply_list.assignment = base_form.cleaned_data['assignment']
            apply_list.base = base_form.cleaned_data['base']
            apply_list.name = base_form.cleaned_data['name']
            apply_list.login_id = base_form.cleaned_data['login_id']
            apply_list.choice_kind = '休日出勤'
            apply_list.plus_work = base_form.cleaned_data['plus_work']
            apply_list.overtime = base_form.cleaned_data['work_time']
            apply_list.email = base_form.cleaned_data['email']
            apply_list.save()

            context = {
                'name': apply_list.name.replace('　', ''),
                'kind': apply_list.choice_kind.replace(' ', ''),
                'lh_adjust': apply_list.plus_work,
            }

            return render(request, 'solu_t/lh_adjust_complete.html', {
                'context': context
            })

        if customize_form.is_valid():
            print('ここまでOK')
            customize_form.send_email()
            apply_list = ApplyList()
            apply_list.base = customize_form.cleaned_data['base']
            print('ここまでOK')
            apply_list.assignment = customize_form.cleaned_data['assignment']
            apply_list.name = customize_form.cleaned_data['name']
            apply_list.login_id = customize_form.cleaned_data['login_id']
            apply_list.choice_kind = '休出 希望'
            apply_list.plus_work = customize_form.cleaned_data['plus_work']
            apply_list.overtime = customize_form.cleaned_data['work_time']
            apply_list.email = customize_form.cleaned_data['email']
            apply_list.save()

            context = {
                'name': apply_list.name.replace('　', ''),
                'kind': apply_list.choice_kind.replace(' ', ''),
                'lh_adjust': apply_list.overtime_date,
                'adjust_date': apply_list.plus_work
            }

            return render(request, 'solu_t/lh_adjust_complete.html', {
                'context': context
            })

        else:
            return HttpResponse('無効なヘッダが検出されました')


class ContactFormView(View):
    template_name = 'solu_t/contact.html'
    success_url = reverse_lazy('mypage')

    def get(self, request, *args, **kwargs):
        user = request.user
        form = ContactForm(initial={
            'name': user.last_name + user.first_name,
            'email': user.email,
            'base': user.base,
        })
        return render(request, 'solu_t/contact.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        if form.is_valid():
            contact_data = ContactData()
            contact_data.name = form.cleaned_data['name']
            contact_data.email = form.cleaned_data['email']
            contact_data.base = form.cleaned_data['base']
            contact_data.message = '{name} さん\n{message}\n'.format(name=form.cleaned_data['name'],
                                                                   message=form.cleaned_data['message'])
            contact_data.contact_kind = form.cleaned_data['kind_contact']
            contact_data.tag = '返信待ち'
            contact_data.save()
            form.send_email()

            context = {
                'name': contact_data.name.replace('　', ''),
                'contact_kind': contact_data.contact_kind,
            }

            return render(request, 'solu_t/contact_complete.html', {
                'context': context
            })

        else:
            return HttpResponse('無効なヘッダが検出されました')


class MypageView(View):
    def get(self, request, *args, **kwargs):
        notice = Notice.objects.order_by('-id')
        reply = ContactData.objects.order_by('-id')
        user = request.user
        return render(request, 'solu_t/mypage.html', {
            'name': user.last_name + user.first_name,
            'user': user,
            'notice': notice,
            'reply': reply,
        })


class UserNoticeDetailView(View):
    def get(self, request, *args, **kwargs):
        notice_data = Notice.objects.get(id=self.kwargs['pk'])
        return render(request, 'solu_t/user_notice_detail.html', {
            'notice_data': notice_data
        })


class ReplyDetailView(View):
    def get(self, request, *args, **kwargs):
        contact_data = ContactData.objects.get(id=self.kwargs['pk'])

        return render(request, 'solu_t/reply_detail.html', {
            'contact_data': contact_data
        })


class ReplyFormView(View):
    def get(self, request, *args, **kwargs):
        contact_data = ContactData.objects.get(id=self.kwargs['pk'])
        reply_form = ContactForm(
            request.POST or None,
            initial={
                'kind_contact': contact_data.contact_kind,
                'base': contact_data.base,
                'name': contact_data.name,
                'email': contact_data.email,
            }
        )

        return render(request, 'solu_t/reply_form.html', {
            'reply_form': reply_form,
            'contact_data': contact_data,
        })

    def post(self, request, *args, **kwargs):
        reply_form = ContactForm(request.POST or None)
        user = request.user

        if reply_form.is_valid():
            contact_data = ContactData.objects.get(id=self.kwargs['pk'])
            contact_data.contact_kind = reply_form.cleaned_data['kind_contact']
            contact_data.base = reply_form.cleaned_data['base']
            contact_data.email = reply_form.cleaned_data['email']
            contact_data.name = reply_form.cleaned_data['name']
            contact_data.message = contact_data.message + '\n\n\n>>> {user} さん\n{message}'.format(
                user=contact_data.name,
                message=
                reply_form.cleaned_data[
                    'message'])
            contact_data.tag = '返信待ち'
            contact_data.save()
            reply_form.send_email()

            context = {
                'name': contact_data.name,
                'contact_kind': contact_data.contact_kind,
            }

            return render(request, 'solu_t/contact_complete.html', {
                'context': context
            })

        else:
            return HttpResponse('無効なヘッダが検出されました')


class ReplyFixView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'solu_t/reply_fix.html')

    def post(self, request, *args, **kwargs):
        contact_data = ContactData.objects.get(id=self.kwargs['pk'])
        contact_data.tag = '解決済み'
        contact_data.save()

        return redirect('mypage')


class StaffRequestShift(View):
    template_name = 'solu_t/day_shift.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        shiftform = ShiftForm(initial={
            'name': user.last_name + '　' + user.first_name,
            'email': user.email,
            'base': user.base,
        })

        return render(request, 'solu_t/day_shift.html', {
            'shiftform': shiftform
        })

    def post(self, request, *args, **kwargs):
        shiftform = ShiftForm(request.POST or None)
        user = request.user

        if shiftform.is_valid():
            shift = ShiftDataModel()
            shift.user_id = user.login_id
            shift.assign = shiftform.cleaned_data['base']
            shift.name = shiftform.cleaned_data['name']
            shift.email = shiftform.cleaned_data['email']
            shift.choice = shiftform.cleaned_data['choice_kind']
            shift.current_day = '・'.join(request.POST.getlist('day'))
            shift.current_time = shiftform.cleaned_data['time']
            shift.firstchoice_day = '・'.join(request.POST.getlist('first_choice_day'))
            shift.firstchoice_time = shiftform.cleaned_data['first_choice_time']
            shift.secondchoice_day = '・'.join(request.POST.getlist('second_choice_day'))
            shift.secondchoice_time = shiftform.cleaned_data['second_choice_time']
            shift.save()

            return render(request, 'solu_t/apply_shift_complete.html', {
                'name': request.user.last_name
            })

        else:
            return HttpResponse('エラーが発生しました。再度申請画面より申請をお願いいたします。')
