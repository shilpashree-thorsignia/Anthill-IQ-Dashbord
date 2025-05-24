from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    source = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name
