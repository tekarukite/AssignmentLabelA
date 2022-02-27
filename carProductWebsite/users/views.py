from django.shortcuts import  render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

def register_request(request):
    if request.method == "POST":
        print(request.POST)
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = CustomUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})