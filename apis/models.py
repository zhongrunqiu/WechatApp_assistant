from django.db import models

# Create your models here.

class App(models.Model):
    appid = models.CharField(primary_key=True,max_length=32)
    category = models.CharField(max_length=128)
    application = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    publish_date = models.DateField()
    url = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)

    def to_dict(self):
        return {
            'appid':self.appid,
            'category':self.category,
            'application':self.application,
            'name':self.name,
            'publish_date':self.publish_date,
            'url':self.url,
            'desc':self.desc,
        }

    def __str__(self):
        return str('{}({})'.format(self.name,self.application))