import json
import requests
import datetime
from django.shortcuts import render,HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
# from .models import premier_users
import csv
import time
import os
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect,HttpResponse,get_object_or_404

import requests
import json
from os import chdir
import xlwt
from .forms import PremierReportForm

from .models import premier_log_refined,Journal_Entry
from .forms import Date_NotesForm,PopupForm
from .forms import BookFormset,DebitFormset,CreditFormset
from .models import Book,Gl_accounts,Approve_Reject

# function to create the gl_accounts of all type
# def save_glaccounts(request):
#     url = "https://momentumcreditltd.sandbox.mambu.com/api/glaccounts?type=ASSET&allowManualJournalEntries=true&activated=true"
#     gl_accounts = requests.get(url, auth=('BACKUPTEST', 'backup123!@#123'))
#     glaccountsjson =gl_accounts.json()


#     for rw in glaccountsjson:
#         encoded_key=rw.get('encodedKey')
#         glcode=rw.get('glCode')
#         name=rw.get('name')

#         Gl_accounts(
#             encoded_key=encoded_key,
#             glCode=glcode,
#             name=name
#         ).save()
#     return HttpResponse('data successfully saved gl-accounts type asset')

# Create your views here.
def create_book_normal(request):
    template_name = 'test/create_normal.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                print(name)
                    
            # once all books are saved, redirect to book list view
            # return redirect('')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })

def journal_entry(request):
    template_name = 'journal_entry.html'
    heading_message = 'JOURNAL ENTRY'
    if request.method == 'GET':
        date_notes_form=Date_NotesForm(request.GET or None)
        debit_formset = DebitFormset(request.GET or None)
        credit_formset = CreditFormset(request.GET or None)
    elif request.method == 'POST':
        date_notes_form=Date_NotesForm(request.POST)
        debit_formset = DebitFormset(request.POST)
        credit_formset = CreditFormset(request.POST)
        if debit_formset.is_valid() and credit_formset.is_valid() and date_notes_form.is_valid():
            for form in debit_formset:
                # extract name from each form and save
                debit = form.cleaned_data.get('debit')
                debit_gl= form.cleaned_data.get('debit_gl')
                debit_branch=form.cleaned_data.get('debit_branch')
                # print(debit,debit_gl,debit_branch)
            for form in credit_formset:
                # extract name from each form and save
                credit = form.cleaned_data.get('credit')
                credit_gl= form.cleaned_data.get('credit_gl')
                credit_branch=form.cleaned_data.get('credit_branch')
                # print(credit,credit_gl,credit_branch)
            entryDate=date_notes_form.cleaned_data.get('entryDate')
            notes=date_notes_form.cleaned_data.get('notes')

            Journal_Entry(
                debit_amount= debit,
                debitglaccount=debit_gl,
                debit_branch=debit_branch,
                credit_amount=credit,
                credit_glaccount=credit_gl,
                credit_branch=credit_branch,
                entry_date=entryDate,
                notes=notes,
                status="pending"
            ).save()
            return HttpResponse('Your journal was successfully created,THANK YOU !')
            
    return render(request, template_name, {
            'credit_formset':credit_formset,
            'debit_formset': debit_formset,
            'journal_form':date_notes_form,
            'heading': heading_message,
            })


def premium_users(request):
    paramdetails = {'fullDetails':'True', 'offset':'0', 'limit':'1000'}
    url = "https://premierkenya.sandbox.mambu.com/api/users"
    
    premier_users = requests.get(url, auth=('api.user', 'apiuser@2018#'))
    premier_usersjson =premier_users.json()
    for rw in premier_usersjson:
        firstName=rw.get('firstName')
        lastName=rw.get('lastName')
        status=rw.get('userState')
        title=rw.get('title')
        email=rw.get('email')

        try:
            branch=rw.get('assignedBranchKey')
        except ObjectDoesNotExist:
            branch=''

        names=str(firstName) + " " + str(lastName)
        premier_users(
            names=names, 
            status=status,
            title=title,
            email=email,
            branch_key=branch
        ).save()
    return HttpResponse('It posted')

def get_csv(request):
    url ="https://premierkenya.mambu.com/api/"
    user = ('DEPAPI', '[7B&HqMchM')
    with open('/home/evans/Desktop/premium/prem/prem_test/static/Assets/Clients-premierkenya.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            clientsurl = url+"clients/{0}".format(', '.join(row))
            client = requests.get(clientsurl, auth=user)
            clientsload = client.json()
        
            assignedBranchkey=clientsload['assignedBranchKey']
            email_add=''
            all_users=premier_users.objects.filter(branch_key=assignedBranchkey)
            for rw in all_users:
                email = rw.email
                title = rw.title
                status = rw.status
                names=rw.names

                if title == 'Branch Manager' and status == 'ACTIVE':
                    email_add = email
                    print(email_add)
        return email_add

# getting premier demand report
def premierdemands_report(request):
    report_form =PremierReportForm(request.POST or None)
    table = [('Account ID', 'Client','TYPE','DATE GENERATED')]

    if report_form.is_valid():
        demand_type = report_form.cleaned_data['demand_type']
        date_from=report_form.cleaned_data['dfrom']
        date_to=report_form.cleaned_data['dto']

        if demand_type=='All':
            results=premier_log_refined.objects.filter(date_generated__range=[date_from,date_to])
        else:
            results = premier_log_refined.objects.filter(date_generated__range=[date_from,date_to],type=demand_type)

        for data in results:
            accountId = data.Account_id
            clientName = data.client
            demandType = data.type
            dateGenerated= data.date_generated

            put = (accountId, clientName, demandType,dateGenerated)                  
            table.append(put)

        if 'Excel' in request.POST:
            fmt_date = xlwt.easyxf(num_format_str='dd/mm/yyyy')
            fmt_datetime = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm:ss')
            fmt_decimal = xlwt.easyxf(num_format_str='#,##0.00')
            fmt_percent = xlwt.easyxf(num_format_str='0.00%')
            fmt_bold = xlwt.easyxf('font: bold on')

            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Demand Report.xls"'
            book = xlwt.Workbook()
            sheet = book.add_sheet('Sheet 1')
            y = 0
            for row in table:
                x = 0
                for cell in row:
                    if sheet.col(x).width < 261 * len(str(cell)):
                        sheet.col(x).width = 261 * len(str(cell))
                    if y == 0:
                        sheet.write(y, x, cell, fmt_bold)
                    elif type(cell) is datetime.datetime:
                        sheet.write(
                            y, x, cell.replace(tzinfo=None), fmt_datetime)
                    elif type(cell) is datetime.date:
                        sheet.write(y, x, cell, fmt_date)
                    elif x == 6:
                        sheet.write(y, x, cell, fmt_decimal)
                    elif x == 7:
                        sheet.write(y, x, cell, fmt_decimal)
                    elif x in (14, 16, 18, 20):
                        sheet.write(y, x, cell, fmt_percent)
                    else:
                        sheet.write(y, x, cell)

                    x += 1
                y += 1
            book.save(response)
            return response

    context= {'table': table, 
        'form': report_form, 
        'title': 'Report'
        }
    context.update(csrf(request))
    return render(request,'reports.html', context)


def journal_approval(request):
    modal_form =PopupForm(request.POST or None)
    journal_data=Journal_Entry.objects.all()
    id =request.POST.get('hidden_id')
    

    if modal_form.is_valid():
        approve_reject =modal_form.cleaned_data['approve_reject']
        reasons=modal_form.cleaned_data['reasons']

    return render(request,'approval.html',
                {'data': journal_data,
                # 'form':modal_form,
                'title': 'Approve Journals'})


def update_status(request,id):
    instance = get_object_or_404(Journal_Entry, id=id)
    form = PopupForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('approve_journal')
    return render(request, 'approval_backup.html', {'form': form}) 
       
    