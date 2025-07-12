from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Trip, JournalEntry
from django import forms
from django.utils import timezone

# Форма для створення/редагування поїздки
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'destination', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Назва поїздки',
            'destination': 'Місце призначення',
            'start_date': 'Дата початку',
            'end_date': 'Дата завершення',
            'description': 'Опис',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("Дата завершення не може бути раніше дати початку.")
        return cleaned_data

# Форма для створення/редагування запису журналу
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry_date', 'content']
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'entry_date': 'Дата запису',
            'content': 'Вміст',
        }

# Список поїздок
def trip_list(request):
    trips = Trip.objects.all().order_by('-created_at')
    return render(request, 'trips/trip_list.html', {'trips': trips})

# Створення поїздки
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поїздку успішно створено!')
            return redirect('trips:trip_list')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = TripForm()
    return render(request, 'trips/create_trip.html', {'form': form})

# Редагування поїздки
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поїздку успішно відредаговано!')
            return redirect('trips:trip_list')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = TripForm(instance=trip)
    return render(request, 'trips/create_trip.html', {'form': form, 'trip': trip})

# Видалення поїздки
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Поїздку успішно видалено!')
        return redirect('trips:trip_list')
    return render(request, 'trips/delete_trip.html', {'trip': trip})

# Журнал подорожей
def journal(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    entries = trip.journal_entries.all().order_by('-entry_date')
    return render(request, 'trips/journal.html', {'trip': trip, 'entries': entries})

# Додавання запису в журнал
def add_journal_entry(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.trip = trip
            entry.save()
            messages.success(request, 'Запис у журналі створено!')
            return redirect('trips:journal', trip_id=trip.id)
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = JournalEntryForm()
    return render(request, 'trips/add_journal_entry.html', {'form': form, 'trip': trip})

# Редагування запису журналу
def edit_journal_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id)
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запис у журналі відредаговано!')
            return redirect('trips:journal', trip_id=entry.trip.id)
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'trips/add_journal_entry.html', {'form': form, 'trip': entry.trip})

# Видалення запису журналу
def delete_journal_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id)
    if request.method == 'POST':
        trip_id = entry.trip.id
        entry.delete()
        messages.success(request, 'Запис у журналі видалено!')
        return redirect('trips:journal', trip_id=trip_id)
    return render(request, 'trips/delete_journal_entry.html', {'entry': entry, 'trip': entry.trip})