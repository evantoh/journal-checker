from django.urls import path

from . import views

urlpatterns = [
    path('data/', views.premium_users, name='premium_users'),
    path('getcsv/', views.get_csv, name='get_csv'),
    path('premierdemands_report/', views.premierdemands_report, name='demand_reports'),
    path('journal_entry/', views.journal_entry, name='journals'),
    path('create_book/', views.create_book_normal, name='book_journal'),
    # path('details/',views. details_form,name="journal_test"),
    path('debit_test/',views.debit_form,name="debit_test"),
    path('journal_approval/',views.journal_approval,name="approve_journal"),

    # path('save_glaccounts/',views.save_glaccounts,name="glaccounts"),
]