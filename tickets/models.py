

from django.db import models
from users.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
    ('OPEN', 'Otwarte'),
    ('IN_PROGRESS', 'W trakcie'),
    ('CLOSED', 'Zamknięte'),
]

    PRIORITY_CHOICES = [
    ('LOW', 'Niski'),
    ('MEDIUM', 'Średni'),
    ('HIGH', 'Wysoki'),
]

    title = models.CharField("Tytuł", max_length=100)
    description = models.TextField("Opis")
    category = models.CharField("Kategoria", max_length=50)
    priority = models.CharField("Priorytet", max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField("Status", max_length=15, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField("Data utworzenia", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()