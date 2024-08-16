from django.shortcuts import render, redirect
from companies.models import Company, Document, Metrics
from .models import InvestmentProposal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404



@login_required
def sugestions(request):    
    areas = Company.area_choices
    if request.method == "GET":
        return render(request, 'sugestions.html', {"areas": areas})
    elif request.method == "POST":
        investor_type = request.POST.get('type')
        area = request.POST.getlist('area')
        value = request.POST.get('value')

        if investor_type == 'C':
            companies = Company.objects.filter(existence_time='+5').filter(phase='E')
        elif investor_type == 'D':
            companies = Company.objects.filter(existence_time__in=['-6', '+6', '+1']).exclude(phase='E')
        elif investor_type == 'G':
            companies = Company.objects.all()

        companies = companies.filter(area__in=area)

        selected_companies = []
        for company in companies:
            percentual = float(value) * 100 / float(company.valuation)
            if percentual >= 1:
                selected_companies.append(company)
                return render(request, 'sugestions.html', {"areas": areas, "companies":selected_companies})


@login_required
def inspect_company(request, id):
    company = Company.objects.get(id=id)
    documents = Document.objects.filter(company=company)
    prop_invest = InvestmentProposal.objects.filter(company=company).filter(status='PA')
    percentual_sold = 0
    for prop in prop_invest:
        percentual_sold += prop.percentual
    
    limiar = (80 * company.percentual_equity) / 100
    concretizado = False
    if percentual_sold >= limiar:
        concretizado =True

    metrics = Metrics.objects.filter(company)

    percentual_disponivel = company.percentual_equity - percentual_sold
    context = {"company": company, "percentual_sold": int(percentual_sold), "concretizado": concretizado, "percentual_disponivel": percentual_disponivel,
               "documents": documents, "metrics": metrics}
    return render(request, 'inspect_company.html', context)


@login_required
def make_proposal(request, id):
    value =request.POST.get('value')
    percentual =request.POST.get('percentual')
    company = Company.objects.get(id=id)

    proposals_accepted = InvestmentProposal.objects.filter(company=company, status='PA')
    total = 0
    for pa in proposals_accepted:
        total += pa.percentual
    
    if total + float(percentual) > company.percentual_equity:
        messages.add_message(request, constants.WARNING, 'O percentual solicitado ultrapassa o percentual máximo')
        return redirect('inspect_company', id)

    valuation = 100 * int(value) / int(percentual)

    if valuation < float(company.valuation / 2):
        messages.add_message(request, constants.WARNING, f'O valuation proposto foi de {valuation:.2f}, o mínimo para a empresa é {int(company.valuation / 2) + 1}')
        return redirect('inspect_company', id)
    
    inv_prop =  InvestmentProposal(
        value=value,
        percentual=percentual,
        company=company,
        investor=request.user
    )
    

    inv_prop.save()
    return redirect('sign_contract', inv_prop.id)



def sign_contract(request, id):
    inv_prop = InvestmentProposal.objects.get(id=id)
    if inv_prop.status != 'AS':
        raise Http404()
    
    if request.method == "GET":
        context ={"id": id, "inv_prop": inv_prop}
        return render(request, 'sign_contract.html', context)
    
    elif request.method == "POST":
        selfie = request.FILES.get('selfie')
        rg = request.FILES.get('rg')

        inv_prop.selfie = selfie
        inv_prop.rg = rg
        inv_prop.status = 'PE'

        inv_prop.save()

        messages.add_message(request, constants.SUCCESS, f'Contrato assinado com sucesso, sua proposta foi enviada a empresa.')
        return redirect('inspect_company', inv_prop.company.id)
    

def manage_proposals(request, id):
    action = request.GET.get('action')

    inv_prop = InvestmentProposal.objects.get(id=id)

    if action == 'accept':
        messages.add_message(request, constants.SUCCESS, 'Proposta aceita')
        inv_prop.status = "PA"
    elif action == "refuse":
        messages.add_message(request, constants.SUCCESS, 'Proposta recusada')
        inv_prop.status = "PR"

    inv_prop.save()
    return redirect('company_details', inv_prop.company.id)