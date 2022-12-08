from django.core.management.base import BaseCommand, CommandError
from solu_t.models import ApplyData

import datetime
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.date.today()
        first_day = today + relativedelta(months=-1, day=1)
        last_day = today + relativedelta(months=0, day=1, days=-1)
        date_before_month = ApplyData.objects.filter(date__date__range=(first_day, last_day))
        holiday = ApplyData.objects.filter(date__holiday_date__range=(first_day, last_day))
        workday = ApplyData.objects.filter(date__work_date__range=(first_day, last_day))
        refresh_day = ApplyData.objects.filter(date__refresh_date__range=(first_day, last_day))
        apply_data = date_before_month.union(holiday, workday, refresh_day)
        apply_data.delete()
        self.stdout.write(self.style.SUCCESS('Successfully delete apply_data'))
