from django.contrib import admin
from .models import User, Conversation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'source', 'timestamp')
    search_fields = ('name', 'phone', 'email', 'session_id')
    list_filter = ('source', 'timestamp')
    readonly_fields = ('timestamp', 'session_id')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'source')
    search_fields = ('user__name', 'user__session_id', 'user_message', 'bot_response')
    list_filter = ('source', 'timestamp')
    readonly_fields = ('timestamp', 'user')
