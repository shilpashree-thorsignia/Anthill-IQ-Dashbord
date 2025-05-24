from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.

@login_required
def dashboard(request):
    users = User.objects.all().order_by('-timestamp')
    context = {
        'users': users,
    }
    return render(request, 'dashboard.html', context)
