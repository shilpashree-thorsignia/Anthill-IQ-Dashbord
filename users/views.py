from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Conversations, Monitors

def dashboard(request):
    users_qs = User.objects.all().order_by('-id')
    return render(request, 'users/dashboard.html', {'users': users_qs})

def chat_history(_, id):
    conversations = Conversations.objects.filter(user_id=id).order_by('timestamp')
    data = {
        'conversations': [
            {
                'user_message': conv.user_message,
                'bot_response': conv.bot_response,
                'timestamp': conv.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for conv in conversations
        ]
    }
    return JsonResponse(data)

def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        monitor = Monitors.objects.filter(name=name, password=password).first()
        if monitor:
            users_qs = User.objects.all().order_by('-id')
            return render(request, 'users/dashboard.html', {'users': users_qs})
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')
