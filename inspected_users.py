DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL:DATABASE_URL: postgresql://postgres:uEutQJRqyRbgOlzwhsGGgczYXaeBqgxI@yamabiko.proxy.rlwy.net:14599/railway
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Users(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
