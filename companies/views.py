from django.shortcuts import render, redirect
from .models import Company, Document, Metrics
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from investors.models import InvestmentProposal
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

@login_required
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


@login_required
def list_companies(request):
    if request.method == "GET":
        company_name  = request.GET.get('company')
        companies = Company.objects.filter(user=request.user)
        if company_name:
            companies = companies.filter(name__icontains=company_name)
        context = {"companies": companies, "company_name": company_name}
        return render(request, 'list_companies.html', context)
        

@login_required
def company_details(request, id):
    company = Company.objects.get(id=id)
    if company.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect('list_companies')
      
    if request.method == "GET":
        documents = Document.objects.filter(company=company)
        inv_prop = InvestmentProposal.objects.filter(company=company)
        inv_prop_sent = inv_prop.filter(status='PE')

        percentual_sold = 0
        for prop in inv_prop:
            if prop.status == "PA":
                percentual_sold += prop.percentual
        
        total_cap =  sum(inv_prop.filter(status="PA").values_list('value', flat=True))

        actual_valuation = (100 * float(total_cap)) / float(percentual_sold) if percentual_sold != 0 else 0
        

        number_of_investors = InvestmentProposal.objects.filter(company=company, status='PA').values('investor').distinct().count()

        context = {"company": company, "documents": documents, "inv_prop_sent": inv_prop_sent, "percentual_sold":int(percentual_sold), 
                   "total_cap": total_cap, "actual_valuation": actual_valuation, "number_of_investors": number_of_investors}
        return render(request, 'company_details.html', context)
    

@login_required    
def add_doc(request, id):
    company = Company.objects.get(id=id)
    title = request.POST.get('title')
    file = request.FILES.get('file')
    extension = file.name.split('.')

    if company.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect('list_companies')  
    
    if extension[1] != "pdf":
        messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
        return redirect('company_details', id)  

    if not file:
        messages.add_message(request, constants.ERROR, 'Selecione um arquivo')
        return redirect('company_details', id)

    document = Document(
        company=company, 
        title=title, 
        file=file)
    document.save()
    messages.add_message(request, constants.SUCCESS, 'Documento cadastrado com sucesso')
    return redirect('company_details', id)


@login_required
def delete_doc(request, id):
    document = Document.objects.get(id=id)
    if document.company.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect('list_companies') 
    document.delete()
    messages.add_message(request, constants.SUCCESS, 'Documento deletado com sucesso')
    return redirect('company_details', document.company.id)


@login_required
def add_metric(request, id):
    company = Company.objects.get(id=id)
    title = request.POST.get('metric_title')
    value = request.POST.get('metric_value')

    if company.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect('list_companies')
    
    metric = Metrics(
        company = company,
        title = title,
        value = value
    )
    metric.save

    messages.add_message(request, constants.SUCCESS, 'Documento deletado com sucesso')
    return redirect('company_details', company.id)


@login_required
def dashbord(request, id):
    company = Company.objects.get(id=id)
    if company.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect('list_companies') 
    today = timezone.now().date()

    seven_days_ago = today - timedelta(days=6)

    proposals_by_day = {}

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)

        proposals = InvestmentProposal.objects.filter(
            company = company,
            status = "PA",
            date = day
        )
        
        total_day = 0
        for proposal in proposals:
            total_day += proposal.value

        proposals_by_day[day.strftime("%d/%m/%Y")] = int(total_day)
    
    context = {'labels': list(proposals_by_day.keys()), 'values': list(proposals_by_day.values())}
    
    return render(request, 'dashbord.html', context)


@login_required
def list_investors(request, id):
    try:
        company = Company.objects.get(id=id)
        if company.user != request.user:
            messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
            return redirect('list_companies') 
        investors = (InvestmentProposal.objects.filter(company=company, status='PA').values('investor__username').annotate(percentual=Sum('percentual')))
        
        context = {'company': company, 'investors': investors}
    except:
        return redirect('dashbord', id)

    return render(request, 'list_investor.html', context)

