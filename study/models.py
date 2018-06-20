from django.db import models


class WordRecord(models.Model):
    proficiency = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    wait = models.PositiveSmallIntegerField(default=0)
    entry = models.ForeignKey('bank.Entry', on_delete=models.CASCADE, related_name='word_records')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='word_records')
