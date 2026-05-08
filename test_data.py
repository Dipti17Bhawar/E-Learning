import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechSutraproj.settings')
django.setup()

from django.contrib.auth.models import User
from TechSutraapp.models import Subject, Resource

# Get superuser or first user to assign upload
user = User.objects.first()
# Get a subject (e.g. SE for Computer Engineering Semester 5)
subject = Subject.objects.filter(name__icontains='Software Engineering').first() or Subject.objects.first()

if subject and user:
    # Add dummy pdf
    Resource.objects.get_or_create(
        subject=subject,
        title='Unit 1 PDF',
        file_type='notes_pdf',
        uploaded_by=user,
        defaults={'file': ''}
    )
    Resource.objects.get_or_create(
        subject=subject,
        title='In-Sem Paper',
        file_type='qp',
        uploaded_by=user,
        defaults={'file': ''}
    )
    Resource.objects.get_or_create(
        subject=subject,
        title='Unit 1 Video',
        file_type='video',
        uploaded_by=user,
        defaults={'file': ''}
    )
    
print("Successfully injected placeholder resources!")
