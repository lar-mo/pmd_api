from django.db import models

class String(models.Model):
    location = models.CharField(max_length=100)
    string_en = models.TextField()
    string_es = models.TextField()
    string_fr = models.TextField()
    string_de = models.TextField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location
