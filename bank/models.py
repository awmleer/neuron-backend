from django.db import models
from django.contrib.postgres.fields import JSONField


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
    english=models.TextField()
    chinese=models.TextField()
    def dict(self):
        return {
            'id':self.id,
            'english':self.english,
            'chinese':self.chinese
        }
    # [stars]


class Repo(models.Model):
    name=models.CharField(max_length=50,default='new repo')
    words=JSONField(default=[]) # TODO remove this
    entries=models.ManyToManyField('Entry',related_name='repos')
    amount=models.IntegerField(default=0) # TODO remove this


class Star(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='stars',db_index=True)
    sentence = models.ForeignKey('Sentence',on_delete=models.CASCADE,related_name='stars',db_index=True)
