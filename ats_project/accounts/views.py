from django.shortcuts import redirect, render
from .models import Registration
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        full_name  = request.POST.get('full_name')
        email_address = request.POST.get('email_address')
        gender = request.POST.get('gender')
        checkBox = request.POST.get('checkbox')=='on'
        print(full_name,email_address,gender,checkBox)

        Registration.objects.create(full_name=full_name,email=email_address,gender=gender,checkBox=checkBox,isHr=False)

        return render(request,'accounts/login.html')
    
    return render(request,'accounts/signup.html')


def login_view(request):
    if request.method=='POST':
        email = request.POST.get('email_address')

        r =Registration.objects.filter(email=email).first()
        
        if r:

            if r.isHr:
                return redirect('/hr_dashboard/')
            else:
                return render(request,'accounts/student.html')
        
        return render(request,'accounts/login.html',{'error':'Invalid email address'})

    return render(request,'accounts/login.html')

def verification_view(request):
    return render(request,'accounts/verification.html')