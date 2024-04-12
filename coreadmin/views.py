from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AdminLoginForm  

def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_admin:  
                    login(request, user)
                    return redirect('scorm-dashboard')  
                else:
                    messages.error(request, "This account doesn't have admin permissions.")
            else:
                messages.error(request, "Invalid username or password.") 
    else:
        form = AdminLoginForm()
    return render(request, 'coreadmin/login.html', {'form': form})

def admin_logout_view(request):
    logout(request)
    return redirect('admin-login')  

