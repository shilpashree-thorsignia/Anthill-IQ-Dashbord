from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Conversations

def dashboard(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'users/dashboard.html', {'users': users})

def chat_history(_, id):
    conversations = Conversations.objects.filter(id=id).order_by('timestamp')
    data = {
        'conversations': [
            {
                'user_message': conv.user_message,
                'bot_response': conv.bot_response,
                'timestamp': conv.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } for conv in conversations
        ]
    }
    return JsonResponse(data)
