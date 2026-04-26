from django.shortcuts import render,redirect
from accounts.models import Registration
from hr_dashboard.models import JobDescriptions

# Create your views here.
def home(request):
    if not request.session.get('is_logged_in'):
        return redirect('accounts:login_view')

    user_id = request.session.get('user_id')
    r = Registration.objects.filter(id=user_id).first()

    return render(request, 'hr_dashboard/index.html', {
        'r': r
    })

def logout_view(request):
    request.session.flush()  # clears all session data
    return redirect('accounts:login_view')


def get_logged_in_user(request):
    if not request.session.get('is_logged_in'):
        return None

    user_id = request.session.get('user_id')
    return Registration.objects.filter(id=user_id).first()


def dashboard(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'hr_dashboard/index.html', {'r': r})

def candidate_detail(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'hr_dashboard/candidate_details.html', {'r': r})


def job_descriptions(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')
    filtered_jobs = JobDescriptions.objects.filter(email = r.email)
    first_job = filtered_jobs.first()
    return render(request, 'hr_dashboard/job_descriptions.html', {'filtered_jobs': filtered_jobs,'first_job':first_job})

def analytics(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'hr_dashboard/analytics.html', {'r': r})

def create_new_job(request):
    if request.method == 'POST':
        # return redirect('hr_dashboard:job_descriptions')
        r = get_logged_in_user(request)

        if not r:
            return redirect('accounts:login_view')

        # Logic to handle job creation would go here
        name = r.full_name
        email = r.email
        company = r.company
        title = request.POST.get('title')
        description = request.POST.get('description')
        required_skills = request.POST.get('skills')
        experience_level = request.POST.get('experience_level')

        JobDescriptions.objects.create(
            name=name,
            email=email,
            company=company,
            title=title,
            description=description,
            required_skills=required_skills,
            experience_level=experience_level,
            active=True)
        print("Job created successfully")
        
    return redirect('hr_dashboard:job_descriptions')

    
