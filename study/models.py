from django.db import models
import time
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class EntryRecord(models.Model):
    proficiency = models.SmallIntegerField(default=-1, db_index=True)
    learned_at = models.DateTimeField(null=True, blank=True, default=None, db_index=True)
    updated_at = models.DateTimeField(null=True, blank=True, default=None, db_index=True)
    entry = models.ForeignKey('bank.Entry', on_delete=models.CASCADE, related_name='entry_records', db_index=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='entry_records', db_index=True)
    next_review_date = models.DateField(null=True, blank=True, default=None, db_index=True)
    starred_sentence_ids = ArrayField(models.PositiveIntegerField(), default=list)
    tags = ArrayField(models.CharField(max_length=5), default=list)

    def flush_updated_at(self):
        self.updated_at = timezone.now()

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
            'learnedAt': self.learned_at.timestamp() if self.updated_at is not None else None,
            'updatedAt': self.updated_at.timestamp() if self.updated_at is not None else None,
            'entry': self.entry.as_dict(),
            'nextReviewDate': int(time.mktime(self.next_review_date.timetuple()))  if self.next_review_date is not None else None,
            'proficiency': self.proficiency,
            'starredSentenceIds': self.starred_sentence_ids,
            'tags': self.tags,
        }

