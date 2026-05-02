from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import Registration, Company  # adjust if your app name is different
from hr_dashboard.models import JobDescriptions  # adjust if your app name is different
from .models import Resume
from .analyser import extract_text_from_resume_and_analyze


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
    companies = Company.objects.all()
    print("Companies is : ",companies)
    if not r:
        return redirect('accounts:login_view')
    

    return render(request, 'candidate_dashboard/upload.html', {'r': r, 'companies': companies})

from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Resume
from hr_dashboard.models import JobDescriptions

def upload_resume(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    if request.method == 'POST':
        resume_file = request.FILES.get('resume')

        if not resume_file:
            print("No resume file uploaded.")
            return redirect('candidate_dashboard:upload')

        company_id = request.POST.get('company')
        jd_id = request.POST.get('jd')

        if not company_id or not jd_id:
            return HttpResponse("Company or JD not selected")

        # ✅ 1. Save Resume (IMPORTANT FIX HERE)
        resume = Resume.objects.create(
            candidate=r,                 # ✅ pass object, not name
            company_id=company_id,       # ✅ use _id shortcut
            jd_id=jd_id,
            resume_file=resume_file
        )

        print("Resume saved:", resume.id)

        analysis_result = extract_text_from_resume_and_analyze(resume.resume_file.path,jd_id)
        print("Analysis Result:", analysis_result)

        resume.is_resume = analysis_result.get('is_resume')
        print("Is Resume:", resume.is_resume)
        resume.score = analysis_result.get('score')
        resume.match_level = analysis_result.get('match_level')
        resume.total_experience  = analysis_result.get('total_experience')

        resume.skills_matched = analysis_result.get('skills', {}).get('matched', [])
        resume.skills_missing = analysis_result.get('skills', {}).get('missing', [])
        resume.skills_extra = analysis_result.get('skills', {}).get('extra', [])
        resume.project_categories = analysis_result.get('project_categories', [])

        resume.suggestions_high = [
            s.get('title') for s in analysis_result.get('suggestions', [])
            if s.get('level') == 'High'
        ]

        resume.suggestions_medium = [
            s.get('title') for s in analysis_result.get('suggestions', [])
            if s.get('level') == 'Medium'
        ]

        resume.suggestions_low = [
            s.get('title') for s in analysis_result.get('suggestions', [])
            if s.get('level') == 'Low'
        ]

        # 🔥 BEST PRACTICE → store full JSON also
        resume.analysis_data = analysis_result

        resume.save()
    

        return redirect('candidate_dashboard:last_result')

    return redirect('candidate_dashboard:upload')





















def get_jds(request):
    company_id = request.GET.get('company_id')
    company = Company.objects.filter(id=company_id)
    if company:
        jds = JobDescriptions.objects.filter(company_id=company_id)
        jd_list = [{'id': jd.id, 'title': jd.title} for jd in jds]
        return JsonResponse({'jds': jd_list})
    return JsonResponse({'jds': []})


def my_resumes(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/my_resumes.html', {'r': r})

def last_result(request):
    r = get_logged_in_user(request)
    last_resume = Resume.objects.filter(candidate=r).order_by('-uploaded_at').first()

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/last_result.html', {'r': r, 'last_resume': last_resume})

def chat_with_resume(request):
    r = get_logged_in_user(request)

    if not r:
        return redirect('accounts:login_view')

    return render(request, 'candidate_dashboard/chat_with_resume.html', {'r': r})