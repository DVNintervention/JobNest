from .models import Profile, JobSeeker, Skill, Language,Company,JobPosting
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.core.files.storage import default_storage

# Create your views here.
def index(request):
    return render(request, 'core/base.html')

def landing_view(request):
    return render(request, 'core/landing_page.html')

class UserLoginView(LoginView):
    template_name = 'core/login.html' 
    success_url = reverse_lazy('core/success') 

def profile_setup(request):
    return render(request, 'core/profile_setup.html')

@login_required
def job_creation(request):
    try:
        company = request.user.company
    except Company.DoesNotExist:
        messages.error(request, "You are not associated with a company.")
        return redirect('some-other-view')

    skills = Skill.objects.all()  

    if request.method == 'POST':
        job_title = request.POST.get('jobTitle')
        location = request.POST.get('location')
        employment_type = request.POST.get('employmentType')
        salary_range = request.POST.get('salaryRange')
        application_deadline = request.POST.get('applicationDeadline')
        about_us = request.POST.get('aboutUs')
        job_description = request.POST.get('jobDescription')
        key_responsibilities = request.POST.get('keyResponsibilities')
        benefits = request.POST.get('benefits')
        how_to_apply = request.POST.get('howToApply')

        job_posting = JobPosting(
            company=company,
            job_title=job_title,
            location=location,
            employment_type=employment_type,
            salary_range=salary_range,
            application_deadline=application_deadline,
            about_us=about_us,
            job_description=job_description,
            key_responsibilities=key_responsibilities,
            benefits=benefits,
            how_to_apply=how_to_apply,
        )
        job_posting.save()
        skill_ids = request.POST.getlist('skills')
        for skill_id in skill_ids:
            skill = Skill.objects.get(id=skill_id)
            job_posting.skills.add(skill)

        messages.success(request, "Job listing created successfully!")
        return redirect('index') 

    return render(request, 'core/job_creation.html', {'skills': skills})

def profile(request):
    return render(request, 'core/profile.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            user.username = email
            user.save()
            messages.success(request, f'Account created for {email}!')

            user = authenticate(username=email, password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)

            return redirect('register_type')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})

@login_required
def register_type(request):
    return render(request,'core/register_type.html')

@login_required
def register_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_description = request.POST.get('company_description')
        address = request.POST.get('address')
        industry = request.POST.get('industry')
        website = request.POST.get('website')
        company_logo = request.FILES.get('company_logo') 

        try:
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.user_type = 'company'
            profile.save()

            company = Company(
                user=request.user,
                company_name=company_name,
                company_description=company_description,
                address=address,
                industry=industry,
                website=website
            )

            if company_logo:
                file_path = default_storage.save(company_logo.name, company_logo)
                company.company_logo = file_path

            company.save()
            messages.success(request, "Company profile created successfully!")
            return redirect('some-success-view')

        except Exception as e:
            messages.error(request, f"Error creating company profile: {str(e)}")

    return render(request, 'core/register_company.html')

@login_required
def register_user(request):
    skills = Skill.objects.all()  
    languages = Language.objects.all()  

    if request.method == 'POST':
        user = request.user  
        profile, created = Profile.objects.get_or_create(user=user)
        profile.user_type = 'jobseeker'
        profile.save()

        jobseeker = JobSeeker(
            user=user,
            address=request.POST['address'],
            phone_number=request.POST['phone_number'],
            education=request.POST['education'],
            academic_status=request.POST['academic_status'],
            #work_experience=request.POST['work_experience'],
            resume_description=request.POST['resume_description']
        )
        jobseeker.save()

        skill_ids = request.POST.getlist('skills')
        for skill_id in skill_ids:
            skill = Skill.objects.get(id=skill_id)
            jobseeker.skills.add(skill)

        language_ids = request.POST.getlist('languages')
        for lang_id in language_ids:
            language = Language.objects.get(id=lang_id)
            jobseeker.languages.add(language)

        return redirect('job_seeker_dashboard')  

    return render(request, 'core/register_user.html', {
        'skills': skills,
        'languages': languages,
    })

from django.http import JsonResponse

def update_resume(request):
    if request.method == 'POST':
        response_data = {'message': 'Resume updated successfully'}
        return JsonResponse(response_data)

    return JsonResponse({})



def display_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    jobseeker = get_object_or_404(JobSeeker, user=user)

    fields_to_display = [
        {"label": "First Name", "value": user.first_name, "field_name": "first_name"},
        {"label": "Last Name", "value": user.last_name, "field_name": "last_name"},
        {"label": "Email", "value": user.email, "field_name": "email"},
        {"label": "Address", "value": jobseeker.address, "field_name": "address"},
        {"label": "Phone Number", "value": jobseeker.phone_number, "field_name": "phone_number"},
        {"label": "Education", "value": jobseeker.education, "field_name": "education"},
        {"label": "Academic Status", "value": jobseeker.academic_status, "field_name": "academic_status"},
        {"label": "Work Experience", "value": jobseeker.work_experience, "field_name": "work_experience"},
        {"label": "Resume Description", "value": jobseeker.resume_description, "field_name": "resume_description"},
    ]

    return render(request, 'core/profile.html', {
        'fields': fields_to_display
    })



def edit_field(request, field_name):
    if request.method == 'POST':

        return redirect('edit_resume')  

    context = {
        'field_name': field_name, 
    }
    return render(request, 'core/edit_field.html', context)

def logout_view(request):
    logout(request)
    return redirect('landing_page')  

@login_required
def job_seeker_dashboard(request):
    try:
        jobseeker = JobSeeker.objects.get(user=request.user)
        jobseeker_skills = jobseeker.skills.all()
        matching_job_postings = JobPosting.objects.filter(skills__in=jobseeker_skills).distinct()
    except JobSeeker.DoesNotExist:
        matching_job_postings = []

    context = {'job_postings': matching_job_postings}
    return render(request, 'core/job_seeker_dashboard.html', context)

def job_posting_detail(request, posting_id):
    posting = get_object_or_404(JobPosting, id=posting_id)
    context = {'posting': posting}
    return render(request, 'core/job_posting_detail.html', context)
