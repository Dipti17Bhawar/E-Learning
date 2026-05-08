import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechSutraproj.settings')
django.setup()

from TechSutraapp.models import Department, Semester, Subject

# Find or create Computer Engineering
dept, created = Department.objects.get_or_create(name='Computer Engineering')

# Create Semesters
sem5, created = Semester.objects.get_or_create(number=5, department=dept)
sem6, created = Semester.objects.get_or_create(number=6, department=dept)

# Add Subjects to Semester 5
sub5_1, _ = Subject.objects.get_or_create(name='Database Management Systems (DBMS)', semester=sem5)
sub5_2, _ = Subject.objects.get_or_create(name='Theory of Computation (TOC)', semester=sem5)
sub5_3, _ = Subject.objects.get_or_create(name='Computer Networks (CN)', semester=sem5)
sub5_4, _ = Subject.objects.get_or_create(name='Software Engineering (SE)', semester=sem5)

# Add Subjects to Semester 6
# (Some might already exist, get_or_create will handle it)
sub6_1, _ = Subject.objects.get_or_create(name='Web Technology (WT)', semester=sem6)
sub6_2, _ = Subject.objects.get_or_create(name='Cloud Computing', semester=sem6)
sub6_3, _ = Subject.objects.get_or_create(name='Data Science and Big Data Analytics', semester=sem6)
sub6_4, _ = Subject.objects.get_or_create(name='Artificial Intelligence (AI)', semester=sem6)

print("Successfully added Semester 5 and Semester 6 with subjects to Computer Engineering!")
