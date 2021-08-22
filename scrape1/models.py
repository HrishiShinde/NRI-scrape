from django.db import models

# Create your models here.
class scrapeData(models.Model):
    dataId = models.AutoField(primary_key = True)
    dataTitle = models.CharField(max_length=20)
    dataTime = models.CharField(max_length = 20)
    dataLink = models.CharField(max_length = 20)
    class Meta:
        db_table = "scrapeData"
