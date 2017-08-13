from django.db import models
import json
# from django.utils import timezone
from django.contrib.postgres.fields import JSONField



class UserInfo(models.Model):
    user=models.OneToOneField('auth.User',on_delete=models.CASCADE,related_name='user_info',db_index=True)
    name = models.CharField(max_length=50, default='新用户')
    def __str__(self):
        return self.name




class Entry(models.Model):
    word=models.CharField(max_length=30,db_index=True)
    level=models.SmallIntegerField()
    definitions=JSONField(default=[])
    definition_rates=JSONField(default={})
    phonetic=JSONField(default={})
    sentencesTemp=JSONField(default=[]) #TODO remove this
    # [sentences]


class Sentence(models.Model):
    entry=models.ForeignKey('Entry',on_delete=models.CASCADE,related_name='sentences',db_index=True)
    text=models.TextField()
    # [stars]


class Star(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='stars',db_index=True)
    sentence = models.ForeignKey('Sentence',on_delete=models.CASCADE,related_name='stars',db_index=True)


class Repo(models.Model):
    name=models.CharField(max_length=50,default='new repo')
    words=JSONField(default=[]) # TODO remove this
    entries=models.ManyToManyField('Entry',related_name='repos')
    amount=models.IntegerField(default=0) # TODO remove this




class SyncData(models.Model):
    user=models.ForeignKey('auth.User',related_name='sync_data')
    sync_time=models.DateTimeField(auto_now=True)
    data=models.TextField(default='{}')
    def set_data(self, x):
        self.data = json.dumps(x)
    def get_data(self):
        return json.loads(self.data)

