from django.db import models

# Create your models here.
class Resume(models.Model):
    candidate = models.ForeignKey('accounts.Registration', on_delete=models.CASCADE)
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)
    jd = models.ForeignKey('hr_dashboard.JobDescriptions', on_delete=models.CASCADE)

    is_resume = models.BooleanField(default=False)
    score = models.IntegerField(blank=True, null=True)
    match_level = models.CharField(max_length=50, blank=True, null=True)
    total_experience  = models.CharField(max_length=100, blank=True, null=True)
    skills_matched = models.JSONField(default=list, blank=True)
    skills_missing = models.JSONField(default=list, blank=True)
    skills_extra = models.JSONField(default=list, blank=True)
    project_categories = models.JSONField(default=list, blank=True)
    suggestions_high = models.JSONField(default=list, blank=True)
    suggestions_medium = models.JSONField(default=list, blank=True)
    suggestions_low = models.JSONField(default=list, blank=True)

    resume_file = models.FileField(upload_to='resumes/')
    # extracted_text = models.TextField(blank=True, null=True)
    # feedback = models.TextField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.company.name} - {self.jd.title}"