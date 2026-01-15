from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Ticket
from .forms import TicketForm, CommentForm


@login_required(login_url='/accounts/login/')
def dashboard(request):
    tickets = Ticket.objects.all()

    if request.user.role == 'USER':
        tickets = tickets.filter(author=request.user)

    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if status:
        tickets = tickets.filter(status=status)
    if priority:
        tickets = tickets.filter(priority=priority)

    open_count = tickets.filter(status='OPEN').count()
    in_progress_count = tickets.filter(status='IN_PROGRESS').count()
    closed_count = tickets.filter(status='CLOSED').count()

    return render(request, 'tickets/dashboard.html', {
        'tickets': tickets,
        'open_count': open_count,
        'in_progress_count': in_progress_count,
        'closed_count': closed_count,
        'total_count': tickets.count()
    })



@login_required(login_url='/accounts/login/')
def ticket_create(request):
    form = TicketForm(request.POST or None)
    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.author = request.user
        ticket.save()
        return redirect('dashboard')

    return render(request, 'tickets/create.html', {
        'form': form
    })


@login_required(login_url='/accounts/login/')
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user.role == 'USER' and ticket.author != request.user:
        return redirect('dashboard')

    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.ticket = ticket
        comment.author = request.user
        comment.save()
        return redirect('ticket_detail', pk=pk)

    return render(request, 'tickets/detail.html', {
        'ticket': ticket,
        'comments': ticket.comments.all(),
        'form': form
    })


ALLOWED_STATUSES = ['OPEN', 'IN_PROGRESS', 'CLOSED']

@login_required
def change_status(request, pk, status):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user.role not in ['ADMIN', 'TECH']:
        return redirect('ticket_detail', pk=pk)

    if status not in ALLOWED_STATUSES:
        return redirect('ticket_detail', pk=pk)

    ticket.status = status
    ticket.save()
    return redirect('ticket_detail', pk=pk)

