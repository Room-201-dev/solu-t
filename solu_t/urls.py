from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('', views.LoginSolutView.as_view(), name='staff_login'),
    path('logout/', views.LogoutSolutView.as_view(), name='staff_logout'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('mypage/change_schedule/', views.ChangeScheduleView.as_view(), name='change_schedule'),
    path('mypage/Sorry_form/', views.SorryFormView.as_view(), name='sorry_form'),
    path('mypage/contact/', views.ContactFormView.as_view(), name='contact'),
    path('mypage/notice/<int:pk>', views.UserNoticeDetailView.as_view(), name='user_notice_detail'),
    path('mypage/plus_work/', views.PlusWorkView.as_view(), name='plus_work'),
    path('mypage/co_oneday/', views.CoOneDayView.as_view(), name='co_oneday'),
    path('mypage/reply/<int:pk>/', views.ReplyDetailView.as_view(), name='user_reply'),
    path('mypage/reply/<int:pk>/reply_form/', views.ReplyFormView.as_view(), name='reply_form'),
    path('mypage/reply/<int:pk>/reply_fix/', views.ReplyFixView.as_view(), name='reply_fix'),
]
