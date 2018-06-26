from django.db import models
import time
from django.utils import timezone


class EntryRecord(models.Model):
    proficiency = models.SmallIntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey('bank.Entry', on_delete=models.CASCADE, related_name='entry_records')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='entry_records')
    next_review_date = models.DateField(null=True, blank=True, default=None)

    def flush_next_review_date(self):
        wait = 1
        if self.proficiency == 0:
            wait = 1
        elif self.proficiency == 1:
            wait = 2
        elif self.proficiency == 2:
            wait = 3
        elif self.proficiency == 3:
            wait = 7
        elif self.proficiency == 4:
            wait = 15
        elif self.proficiency == 5:
            wait = 30
        elif self.proficiency == 6:
            wait = 60
        elif self.proficiency == 7:
            wait = 120
        elif self.proficiency == 8:
            wait = -1
        if wait == -1:
            self.next_review_date = None
        else:
            self.next_review_date = timezone.now() + timezone.timedelta(days=wait)

    def as_dict(self):
        return {
            'id': self.id,
            'createdAt': self.created_at.timestamp(),
            'entry': self.entry.as_dict(),
            'nextReviewDate': int(time.mktime(self.next_review_date.timetuple())),
            'proficiency': self.proficiency
        }

