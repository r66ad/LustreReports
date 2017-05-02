import datetime

from django.utils import timezone
from django.test import TestCase

from reports.models import ostPerfHistory


class ReportsMethodTests(TestCase):

    def test_was_created_recently(self):
        """
        was_created_recently() should return False for reports whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = ostPerfHistory(timepoint=time)
        self.assertIs(future_question.is_recent(), False)
