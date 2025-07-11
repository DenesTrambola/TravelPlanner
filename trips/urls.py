from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('create/', views.create_trip, name='create_trip'),
    path('edit/<int:trip_id>/', views.edit_trip, name='edit_trip'),
    path('delete/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('journal/<int:trip_id>/', views.journal, name='journal'),
    path('journal/<int:trip_id>/add/', views.add_journal_entry, name='add_journal_entry'),
    path('journal/edit/<int:entry_id>/', views.edit_journal_entry, name='edit_journal_entry'),
    path('journal/delete/<int:entry_id>/', views.delete_journal_entry, name='delete_journal_entry'),
]