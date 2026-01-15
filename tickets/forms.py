
from django.forms import ModelForm
from .models import Ticket
class TicketForm(ModelForm):
    class Meta:
        model=Ticket
        fields=['title','description','category','priority']
        labels = {
            'title': 'Tytuł',
            'description': 'Opis',
            'category': 'Kategoria',
            'priority': 'Priorytet'
        }

from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Treść komentarza:'
        }

