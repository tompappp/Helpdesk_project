from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.role = 'USER'
        user.save()
        return redirect('/accounts/login/')
    return render(request, 'registration/register.html', {'form': form})
