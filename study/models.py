from django.db import models
import time


class EntryRecord(models.Model):
    proficiency = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey('bank.Entry', on_delete=models.CASCADE, related_name='entry_records')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='entry_records')
    next_review_date = models.DateField(null=True, blank=True, default=None)
    def as_dict(self):
        return {
            'id': self.id,
            'createdAt': self.created_at.timestamp(),
            'entry': self.entry.as_dict(),
            'nextReviewDate': int(time.mktime(self.next_review_date.timetuple())),
            'proficiency': self.proficiency
        }

