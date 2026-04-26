import random
from urllib import request
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import Registration
from django.contrib.auth.decorators import login_required
from decouple import config


# Create your views here.
def generate_otp():
    return random.randint(100000, 999999)

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
        
        otp = generate_otp()
        request.session['otp'] = otp
        request.session['email'] = email

        send_mail(
        subject='🔑 Your OTP for AI Resume ATS',
        message=f"""\
        Hello {email},

        Welcome to AI Resume ATS!

        Your One-Time Password (OTP) is:

        {otp}

        This OTP is valid for a short time. Please enter it on the verification page to complete your login.

        If you did not request this, you can safely ignore this email.

        Thanks & Regards,
        AI Resume ATS Team
        """,
            from_email=config('EMAIL_HOST_USER'),
            recipient_list=[email],
            fail_silently=False
        )
        return render(request,'accounts/verification.html',context={'email':email}  )
        # if r:

        #     if r.isHr:
        #         return redirect('/hr_dashboard/')
        #     else:
        #         return render(request,'accounts/student.html')
        
    return render(request,'accounts/login.html',{'error':'Invalid email address'})

    # return render(request,'accounts/login.html')

def verify_otp(request):
    
    if request.method == "GET":
        return redirect('login_view')
    
    if request.method == "POST":
        entered_otp = ''.join([
            request.POST.get('otp1', ''),
            request.POST.get('otp2', ''),
            request.POST.get('otp3', ''),
            request.POST.get('otp4', ''),
            request.POST.get('otp5', ''),
            request.POST.get('otp6', '')
        ])

        session_otp = str(request.session.get('otp'))
        email = request.session.get('email')

        if not session_otp or not email:
            return redirect('login_view')
        
        if entered_otp == session_otp:
            r = Registration.objects.filter(email=email).first()
            request.session['is_logged_in'] = True
            request.session['user_id'] = r.id
            request.session['user_email'] = r.email
            request.session['is_hr'] = r.isHr
            request.session.set_expiry(60 * 30)
            if r:
                if r.isHr:
                    return redirect('/hr_dashboard/')
                else:
                    return render(request,'accounts/student.html')
        else:
            return render(request,'accounts/verification.html',{'error':'Incorrect OTP. Please try again.', 'email': email})
        
def resend_otp(request):
    otp = generate_otp()
    request.session['otp'] = otp
    request.session['otp_email'] = email
    request.session.set_expiry(60) 
    email = request.session.get('email')

    send_mail(
            subject='🔑 Your OTP for AI Resume ATS',
            message=f"""
                Hello {email},

                Welcome to AI Resume ATS! Your One-Time Password (OTP) is:

                        {otp}

                Please enter this OTP on the verification page to complete your login.

                If you did not request this, please ignore this email.

                Thanks,
                AI Resume ATS Team
                """,
            from_email=config('EMAIL_HOST_USER'),
            recipient_list=[email],
            fail_silently=False
        )
    return render(request,'accounts/verification.html',context={'email':email}  )
