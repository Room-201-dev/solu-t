from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('login/', views.LoginManagerView.as_view(), name='manager_login'),
    path('logout/', views.LogoutManagerView.as_view(), name='manager_logout'),
    path('login/manager_page/', views.ManagerPageView.as_view(), name='manager_page'),
    path('login/manager_page/post_notice/', views.PostNoticeView.as_view(), name='post_notice'),
    path('login/manager_page/notice_list/', views.NoticeListView.as_view(), name='notice_list'),
    path('login/manager_page/notice_detail/<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('login/manager_page/notice_detail/<int:pk>/notice_edit', views.NoticeEditView.as_view(), name='notice_edit'),
    path('login/manager_page/notice_detail/<int:pk>/notice_delete/', views.NoticeDeleteView.as_view(),
         name='notice_delete'),
    path('login/manager_page/apply_data', views.ApplyListView.as_view(), name='apply_data'),
    path('login/manager_page/apply_data/export', views.export, name='export_excel'),
    path('login/manager_page/apply_tyo4_thismonth/', views.ApplyTYO4ThisMonthView.as_view(),
         name='apply_tyo4_thismonth'),
    path('login/manager_page/apply_tyo4_nextmonth/', views.ApplyTYO4NextMonthView.as_view(),
         name='apply_tyo4_nextmonth'),
    path('login/manager_page/apply_tyo4_twomonth/', views.ApplyTYO4TwoMonthView.as_view(), name='apply_tyo4_twomonth'),
    path('login/manager_page/apply_tyo6_thismonth/', views.ApplyTYO6ThisMonthView.as_view(),
         name='apply_tyo6_thismonth'),
    path('login/manager_page/apply_tyo6_nextmonth/', views.ApplyTYO6NextMonthView.as_view(),
         name='apply_tyo6_nextmonth'),
    path('login/manager_page/apply_tyo6_twomonth/', views.ApplyTYO6TwoMonthView.as_view(), name='apply_tyo6_twomonth'),
    path('login/manager_page/apply_tyo8_thismonth/', views.ApplyTYO8ThisMonthView.as_view(),
         name='apply_tyo8_thismonth'),
    path('login/manager_page/apply_tyo8_nextmonth/', views.ApplyTYO8NextMonthView.as_view(),
         name='apply_tyo8_nextmonth'),
    path('login/manager_page/apply_tyo8_twomonth/', views.ApplyTYO8TwoMonthView.as_view(), name='apply_tyo8_twomonth'),
    path('login/manager_page/contact_list/', views.ContactListView.as_view(), name='contact_list'),
    path('login/manager_page/contact_list/contact_detail/<int:pk>/', views.ContactDetailView.as_view(),
         name='contact_detail'),
    path('login/manager_page/contact_list/contact_detail/<int:pk>/reply', views.ContactReplyView.as_view(),
         name='reply'),
    path('login/manager_page/contact_list/contact_detail/<int:pk>/delete', views.DeleteContactView.as_view(),
         name='delete_contact'),
    path('login/manager_page/contact_list/search/', views.SearchContactView.as_view(), name='contact_search')
]
