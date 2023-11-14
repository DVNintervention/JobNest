from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Profile, JobSeeker, Skill, Language
from django.contrib.auth import logout
from django.shortcuts import redirect
from core.models import JobSeeker
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from core.models import JobSeeker, WorkExperience

# Create your views here.
def index(request):
    return render(request, 'core/base.html')

def landing_view(request):
    return render(request, 'core/landing_page.html')

class UserLoginView(LoginView):
    template_name = 'core/login.html' # Provide the path to your login template here
    success_url = reverse_lazy('core/success') # Provide the name of the URL to redirect after successful login

def profile_setup(request):
    return render(request, 'core/profile_setup.html')

def job_creation(request):
    return render(request, 'core/job_creation.html')

def profile(request):
    return render(request, 'core/profile.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Do not save the form directly to the database yet
            email = form.cleaned_data.get('email')
            user.username = email  # Set the email as username
            user.save()  # Save the user object to the database
            messages.success(request, f'Account created for {email}!')
            return redirect('core/register_company.html')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def register_type(request):
    return render(request,'core/register_type.html')

@login_required
def register_company(request):
    return render(request,'core/register_company.html')

@login_required
def register_user(request):
    if request.method == 'POST':
        user = request.user  # Fetch the user from the request object

        # Create or update a Profile object and set user_type to 'jobseeker'
        profile, created = Profile.objects.get_or_create(user=user)
        profile.user_type = 'jobseeker'
        profile.save()

        # Assuming you haven't created a JobSeeker instance for this user yet
        jobseeker = JobSeeker(user=user, address=request.POST['address'], phone_number=request.POST['phone_number'], education=request.POST['education'], academic_status=request.POST['academic_status'], work_experience=request.POST['work_experience'], resume_description=request.POST['resume_description'])
        jobseeker.save()

        # Handle skills as text input:
        skill_names = request.POST.getlist('skills')
        for skill_name in skill_names:
            skill, created = Skill.objects.get_or_create(name=skill_name.strip())
            jobseeker.skills.add(skill)

        # For ManyToMany fields like languages, if they are fetched as IDs:
        languages = request.POST.getlist('languages')
        for lang_id in languages:
            language = Language.objects.get(id=lang_id)
            jobseeker.languages.add(language)

        # Redirect the user to a success page or dashboard after profile completion
        return redirect('profile')  # Assuming the name of the URL pattern for the profile page is 'profile'

    # Render the registration form if it's a GET request
    return render(request, 'register_user')

from django.http import JsonResponse

def update_resume(request):
    if request.method == 'POST':
        # In this example, we don't perform any server-side processing
        # You can add your own logic here if needed
        
        # Return a JSON response indicating that the resume has been updated
        response_data = {'message': 'Resume updated successfully'}
        return JsonResponse(response_data)

    # If the request method is not POST, return an empty response
    return JsonResponse({})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from core.models import JobSeeker, WorkExperience

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
        # ... add other fields similarly ...
    ]

    return render(request, 'core/profile.html', {
        'fields': fields_to_display
    })


from django.shortcuts import render, redirect

def edit_field(request, field_name):
    if request.method == 'POST':
        # Handle form submission and update the field in the database
        # Redirect back to the "Edit Resume" page after saving changes
        return redirect('edit_resume')  # Replace 'edit_resume' with your actual URL name

    # Render the field editing form template
    context = {
        'field_name': field_name,  # You can use this context variable in the template to determine which field is being edited
    }
    return render(request, 'core/edit_field.html', context)

def logout_view(request):
    logout(request)
    return redirect('landing_page')  # Redirect to the home page (or any other page you'd like).