from django.shortcuts import render
from .models import User

# Create your views here.

def dashboard(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'users/dashboard.html', {'users': users})
