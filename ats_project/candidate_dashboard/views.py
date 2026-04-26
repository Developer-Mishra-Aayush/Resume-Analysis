from django.shortcuts import render, redirect
from accounts.models import Registration  # adjust if your app name is different


def get_logged_in_user(request):
    if not request.session.get('is_logged_in'):
        return None

    user_id = request.session.get('user_id')
    return Registration.objects.filter(id=user_id).first()


def candidate_dashboard(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/dashboard.html', {'r': r})

def upload(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/upload.html', {'r': r})


def my_resumes(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/my_resumes.html', {'r': r})

def last_result(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/last_result.html', {'r': r})

def chat_with_resume(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/chat_with_resume.html', {'r': r})