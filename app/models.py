from django.db import models
import json



class SyncData(models.Model):
    user=models.ForeignKey('auth.User',related_name='sync_data', on_delete=models.SET_NULL, null=True)
    sync_time=models.DateTimeField(auto_now=True)
    data=models.TextField(default='{}')
    def set_data(self, x):
        self.data = json.dumps(x)
    def get_data(self):
        return json.loads(self.data)

