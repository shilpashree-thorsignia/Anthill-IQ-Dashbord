from django.db import models
from django.contrib.auth.models import User as AuthUser

class User(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    session_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'users'
        managed = False
        app_label = 'analytics'
        constraints = [
            models.UniqueConstraint(fields=['session_id'], name='unique_session_id')
        ]

    def __str__(self):
        return f"{self.name or 'Unknown'} ({self.phone or 'No Phone'})"

class Conversation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations',
        db_column='user_id',
        to_field='session_id'
    )
    user_message = models.TextField(blank=True, null=True)
    bot_response = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'conversations'
        managed = False
        app_label = 'analytics'

    def __str__(self):
        return f"Conversation {self.id} - {self.timestamp}"
