from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Conversations, Monitors

def dashboard(request):
    users_qs = User.objects.all().order_by('-id')
    return render(request, 'users/dashboard.html', {'users': users_qs})

from django.shortcuts import render, get_object_or_404
from .models import Conversations

def display_conversation(request, id):
    conversation = get_object_or_404(Conversations, id=id)
    context = {
        'conversation': conversation
    }
    return render(request, 'users/conversation_detail.html', context)


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
