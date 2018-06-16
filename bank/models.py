from django.db import models
from django.contrib.postgres.fields import JSONField


class Entry(models.Model):
    word = models.CharField(max_length=30, db_index=True, unique=True)
    rank = models.SmallIntegerField(null=True, default=None)
    definitions = JSONField(default=[])
    pronounce = JSONField(default={})
    # [sentences]
    def as_dict(self):
        sentences = []
        for s in self.sentences.all():
            sentences.append(s.as_dict())
        return {
            'id': self.id,
            'word': self.word,
            'rank': self.rank,
            'definitions': self.definitions,
            'pronounce': self.pronounce,
            'sentences': sentences
        }


class Sentence(models.Model):
    entry = models.ForeignKey('Entry',on_delete=models.CASCADE,related_name='sentences',db_index=True)
    english = models.TextField()
    chinese = models.TextField()
    reference = models.TextField(default='')
    def as_dict(self):
        return {
            'id':self.id,
            'english':self.english,
            'chinese':self.chinese
        }
    # [stars]


class Repo(models.Model):
    name=models.CharField(max_length=50, default='new repo', unique=True, db_index=True)
    entries=models.ManyToManyField('Entry', related_name='repos')
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.entries.count()
        }


class SentenceStar(models.Model):
    user = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name='sentence_stars',db_index=True)
    sentence = models.ForeignKey('Sentence',on_delete=models.CASCADE,related_name='stars',db_index=True)
