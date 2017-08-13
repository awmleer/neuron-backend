from django.db import models
import json
# from django.utils import timezone
from django.contrib.postgres.fields import JSONField



class UserInfo(models.Model):
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='user_info')
    name = models.CharField(max_length=50, default='新用户')
    def __str__(self):
        return self.name




class Entry(models.Model):
    word=models.CharField(max_length=30)
    level=models.SmallIntegerField()
    definitions=JSONField(default=[])
    definition_rates=JSONField(default={})
    phonetic=JSONField(default={})
    sentences=JSONField(default=[])



class Repo(models.Model):
    name=models.CharField(max_length=50,default='new repo')
    words=models.TextField(default=[])
    amount=models.IntegerField(default=0)
    def set_words(self, x):
        self.words = json.dumps(x)
    def get_words(self):
        return json.loads(self.words)



class SyncData(models.Model):
    user=models.ForeignKey('auth.User',related_name='sync_data')
    sync_time=models.DateTimeField(auto_now=True)
    data=models.TextField(default={})
    def set_data(self, x):
        self.data = json.dumps(x)
    def get_data(self):
        return json.loads(self.data)

