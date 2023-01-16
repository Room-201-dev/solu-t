from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Notice, ApplyList, ApplyData, ContactData, ShiftDataModel

# Register your models here.

CustomUser = get_user_model()


def notify(modeladmin, request, queryset):
    for post in queryset:
        post.email_push(request)


class PostAdmin(admin.ModelAdmin):
    actions = [notify]


admin.site.register(CustomUser)
admin.site.register(Notice, PostAdmin)
admin.site.register(ApplyList)
admin.site.register(ApplyData)
admin.site.register(ContactData)
admin.site.register(ShiftDataModel)
