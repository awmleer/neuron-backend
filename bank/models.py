from django.db import models
from django.contrib.postgres.fields import JSONField


class Entry(models.Model):
    word=models.CharField(max_length=30,db_index=True)
    level=models.SmallIntegerField()
    definitions=JSONField(default=[])
    definition_rates=JSONField(default={})
    phonetic=JSONField(default={})
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
    entries=models.ManyToManyField('Entry',related_name='repos')


class SentenceStar(models.Model):
    user = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='sentence_stars',db_index=True)
    sentence = models.ForeignKey('Sentence',on_delete=models.CASCADE,related_name='stars',db_index=True)
