from django.shortcuts import render
from companies.models import Company

# Create your views here.

def sugestions(request):    
    areas = Company.area_choices
    if request.method == "GET":
        return render(request, 'sugestions.html', {"areas": areas})
    elif request.method == "POST":
        investor_type = request.POST.get('type')
        area = request.POST.get('area')
        value = request.POST.get('value')

        if investor_type == 'C':
            companies = Company.objects.filter(existence_time='+5').filter(stage='E')
        elif investor_type == 'D':
            companies = Company.objects.filter(existence_time__in=['-6', '+6', '+1']).exclude(stage='E')
