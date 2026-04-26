from django.shortcuts import render,redirect
from accounts.models import Registration

# Create your views here.
def home(request):
    if not request.session.get('is_logged_in'):
        return redirect('login_view')

    user_id = request.session.get('user_id')
    r = Registration.objects.filter(id=user_id).first()

    return render(request, 'hr_dashboard/index.html', {
        'r': r
    })

def logout_view(request):
    request.session.flush()  # clears all session data
    return redirect('accounts:login_view')