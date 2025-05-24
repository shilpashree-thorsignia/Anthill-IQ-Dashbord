from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Contact, Assessment, Career

# Create your views here.

@login_required
def dashboard(request):
    contacts = Contact.objects.all().order_by('-created_at')
    assessments = Assessment.objects.all().order_by('-created_at')
    careers = Career.objects.all().order_by('-created_at')
    
    context = {
        'contacts': contacts,
        'assessments': assessments,
        'careers': careers,
    }
    return render(request, 'dashboard.html', context)
