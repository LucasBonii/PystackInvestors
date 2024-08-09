from django.shortcuts import render, redirect
from .models import Company
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.

def register_company(request):
    if request.method == "GET":

        context = {"existence_time": Company.existence_time_choices,
                   "areas": Company.area_choices}
        
        return render(request, "register_company.html", context)
    elif request.method == "POST":
        name = request.POST.get('name')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        existence_time = request.POST.get('existence_time')
        description = request.POST.get('description')
        end_of_capture = request.POST.get('final_date')
        percentual_equity = request.POST.get('percentual_equity')
        phase = request.POST.get('phase')
        area = request.POST.get('area')
        target_audience = request.POST.get('target_audience')
        value = request.POST.get('value')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')
        try:
            company = Company(
                user = request.user,
                name = name,
                cnpj = cnpj,
                site = site,
                existence_time = existence_time,
                description = description,
                end_of_capture = end_of_capture,
                percentual_equity = percentual_equity,
                phase = phase,
                area = area,
                target_audience = target_audience,
                value = value,
                pitch = pitch,
                logo = logo,
                )
            company.save()
        except:
            messages.add_message(request, constants.ERROR, 'Erro no servidor')
            return redirect('register_company')
        
        messages.add_message(request, constants.SUCCESS, 'Empresa criada com sucesso!')
        return redirect('register_company')
    

def list_companies(request):
    if request.method == "GET":
        return render(request, 'list_companies.html')
        
           