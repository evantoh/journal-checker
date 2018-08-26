from django.contrib import admin
from . models import Journal_Entry,premier_log_refined,Book,Gl_accounts,Approve_Reject
# Register your models here.
admin.site.register(Journal_Entry)
admin.site.register(premier_log_refined)
admin.site.register(Book)
admin.site.register(Gl_accounts)
admin.site.register(Approve_Reject)