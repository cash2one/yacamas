from django.db import models

class TabA(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    tb = models.ManyToManyField('TabB')
    tc = models.ManyToManyField('TabC')
    

class TabB(models.Model):
    path = models.CharField(max_length=239)
    file_name = models.CharField(max_length=60)
    ref_cnt = models.PositiveSmallIntegerField(default=0)
    id_forever = models.BooleanField(default=False)

class TabC(models.Model):
    utitle = models.CharField(max_length=60)
    ucontent = models.TextField()

