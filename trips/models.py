from django.db import models

class Trip(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва поїздки")
    destination = models.CharField(max_length=100, verbose_name="Місце призначення")
    start_date = models.DateField(verbose_name="Дата початку")
    end_date = models.DateField(verbose_name="Дата завершення")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Поїздка"
        verbose_name_plural = "Поїздки"

class JournalEntry(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="journal_entries", verbose_name="Поїздка")
    entry_date = models.DateField(verbose_name="Дата запису")
    content = models.TextField(verbose_name="Вміст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"Запис від {self.entry_date} для {self.trip.title}"

    class Meta:
        verbose_name = "Запис у журналі"
        verbose_name_plural = "Записи у журналі"