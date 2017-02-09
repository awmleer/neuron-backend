from django.db import models
import json


# Create your models here.
class Entry(models.Model):
    word=models.CharField(max_length=30)
    level=models.SmallIntegerField()
    definitions=models.CharField(max_length=800,default='[]')  #用json字符串存储的联系人列表
    def set_definitions(self, x):
        self.definitions = json.dumps(x)
    def get_definitions(self):
        return json.loads(self.definitions)
    phonetic=models.CharField(max_length=1000,default='{}')  #用json字符串存储的联系人列表
    def set_phonetic(self, x):
        self.phonetic = json.dumps(x)
    def get_phonetic(self):
        return json.loads(self.phonetic)
    sentences=models.CharField(max_length=3000,default='[]')  #用json字符串存储的联系人列表
    def set_sentences(self, x):
        self.sentences = json.dumps(x)
    def get_sentences(self):
        return json.loads(self.sentences)

