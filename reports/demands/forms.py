from django import forms
import datetime
import requests
from .models import Journal_Entry
from django.forms import formset_factory
from .models import Gl_accounts



class PremierReportForm(forms.Form): 
    TYPES  = [
        ('', '--------------'),
        ('All','All'),
        ('Demand One ','Demand One'),
        ('Demand Two ','Demand Two'),
        ('Guarantor One ','Guarantor_One'),
        ('Guarantor Two','Guarantor Two'),
        ('Recall','Recall')
    ]
    demand_type = forms.ChoiceField(required=False, label='Types', choices=TYPES)
    dfrom = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }), label='From (YYYY/MM/DD)')
    dto = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }), label='To (YYYY/MM/DD)')


 

# approval form
class PopupForm(forms.ModelForm):
    class Meta:
        model =Journal_Entry
        fields = ('status',) 

 

class BookForm(forms.Form):
    name = forms.CharField(
        label='Book Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    )
BookFormset = formset_factory(BookForm, extra=1)


class DebitForm(forms.Form):
    branches_url="https://momentumcreditltd.sandbox.mambu.com/api/branches"
    branches=requests.get(branches_url,auth=('BACKUPTEST', 'backup123!@#123'))
    branches_load=branches.json()
    TYPES  = []

    for rw in branches_load:
        encodedKey=rw.get('encodedKey')
        name= rw.get('name')
        TYPES.append([str(name),str(name)])

    TYPE_BRANCH = [('', '-------------------------------')] + TYPES

    TYPES_GL=[]
    gl_accounts=Gl_accounts.objects.all()
    for rw in gl_accounts:
        encoded_key=rw.encoded_key
        glcode=rw.glCode
        name=rw.name
        TYPES_GL.append([encoded_key,(glcode +' '+ '-'+' '+ name)])
        
    TYPE_GLACCOUNT = [('', '-------------------------------')] + TYPES_GL
    debit = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': 'Amount in Ksh',
            'class' : 'debitform'

        })
    )
    debit_gl = forms.ChoiceField(
            required=True,
            label='',
            choices=TYPE_GLACCOUNT,
            widget=forms.Select(attrs={
                'class':'debit_glform'
                })
        )
    
    debit_branch = forms.ChoiceField(
            required=True,
            label='',
            choices=TYPE_BRANCH,
            widget=forms.Select(attrs={
                'class':'debit_branch'
                })
        )  
DebitFormset = formset_factory(DebitForm, extra=1)

class CreditForm(forms.Form):
    branches_url="https://momentumcreditltd.sandbox.mambu.com/api/branches"
    branches=requests.get(branches_url,auth=('BACKUPTEST', 'backup123!@#123'))
    branches_load=branches.json()
    TYPES  = []

    for rw in branches_load:
        encodedKey=rw.get('encodedKey')
        name= rw.get('name')
        TYPES.append([str(name),str(name)])

    TYPE_BRANCH = [('', '-------------------------------')] + TYPES

    TYPES_GL=[]
    gl_accounts=Gl_accounts.objects.all()
    for rw in gl_accounts:
        encoded_key=rw.encoded_key
        glcode=rw.glCode
        name=rw.name
        TYPES_GL.append([encoded_key,(glcode +' '+ '-'+' '+ name)])
        
    TYPE_GLACCOUNT = [('', '-------------------------------')] + TYPES_GL
    credit = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': 'Amount in Ksh',
            'class' : 'creditform'

        })
    )
    credit_gl = forms.ChoiceField(
            required=True,
            label='',
            choices=TYPE_GLACCOUNT,
            widget=forms.Select(attrs={
                'class':'credit_glform'
                })
        )
    
    credit_branch = forms.ChoiceField(
            required=True,
            label='',
            choices=TYPE_BRANCH,
            widget=forms.Select(attrs={
                'class':'credit_branch'
                })
        )  
CreditFormset = formset_factory(CreditForm, extra=1)

class Date_NotesForm(forms.Form):
    entryDate = forms.DateField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class':'datepicker',
            'placeholder': 'Entry Dates',
            })
        )
    notes = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'class' : 'notesform',
            'placeholder': 'Notes',
            })
        )