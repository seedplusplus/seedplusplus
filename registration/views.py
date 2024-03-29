from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required



class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    
def profile_page(request):
    context = {}
    return render(request, "profile.html", context)


@login_required
def delete_self(request):
    user = request.user
    user.is_active = False
    user.save()

    return redirect('logout')
