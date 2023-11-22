from django.db import models
from django.contrib.auth.models import User,AbstractUser


class Profile(models.Model):
    USER_TYPES = (
        ('jobseeker', 'JobSeeker'),
        ('company', 'Company'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)


class WorkExperience(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    jobseeker = models.ForeignKey('JobSeeker', on_delete=models.CASCADE)


class JobSeeker(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    academic_status = models.CharField(max_length=255)
    work_experience = models.CharField(max_length=255)
    skills = models.ManyToManyField(Skill)
    languages = models.ManyToManyField(Language)
    resume_description = models.CharField(max_length=255)


class Company(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_logo = models.BinaryField()
    company_description = models.TextField()
    address = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    website = models.URLField()

class JobPosting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50) 
    salary_range = models.CharField(max_length=100, blank=True, null=True)  
    application_deadline = models.DateField()
    about_us = models.TextField(blank=True, null=True)  
    job_description = models.TextField()
    skills = models.ManyToManyField(Skill) 
    key_responsibilities = models.TextField()
    benefits = models.TextField(blank=True, null=True)  
    how_to_apply = models.TextField()


class Chat(models.Model):
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField()


class Message(models.Model):
    JOBSEEKER = 'jobseeker'
    COMPANY = 'company'
    SENDER_TYPE_CHOICES = [
        (JOBSEEKER, 'Jobseeker'),
        (COMPANY, 'Company'),
    ]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender_id = models.IntegerField()
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE_CHOICES)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)


class JobApplication(models.Model):
    PENDING = 'pending'
    REVIEWED = 'reviewed'
    INTERVIEWED = 'interviewed'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REVIEWED, 'Reviewed'),
        (INTERVIEWED, 'Interviewed'),
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
    ]

    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    cover_letter = models.TextField()
    additional_notes = models.TextField()
