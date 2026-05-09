from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import UserRegistrationData, Department, Semester, Subject, Resource, PlatformReview, VideoLecture

# Create your views here.
def home(request):
    return render(request, 'TechSutraapp/home.html')

def about(request):
    return render(request, 'TechSutraapp/about.html')

@login_required(login_url='login')
def platform_reviews(request):
    if request.method == "POST":
        review_text = request.POST.get('reviewText')
        rating = request.POST.get('rating')
        if review_text and rating:
            PlatformReview.objects.create(
                user=request.user,
                rating=int(rating),
                text=review_text
            )
            messages.success(request, "Review submitted successfully!")
            return redirect('reviews')
            
    reviews = PlatformReview.objects.all().order_by('-created_at')
    return render(request, 'TechSutraapp/reviews.html', {'reviews': reviews})

@login_required(login_url='login')
def video_lectures(request):
    """View all video lectures across all subjects"""
    video_lectures = VideoLecture.objects.all().select_related('subject', 'subject__semester', 'subject__semester__department', 'uploaded_by').order_by('-created_at')

    # Group by department for better organization
    videos_by_department = {}
    for video in video_lectures:
        dept_name = video.subject.semester.department.name
        if dept_name not in videos_by_department:
            videos_by_department[dept_name] = []
        videos_by_department[dept_name].append(video)

    context = {
        'videos_by_department': videos_by_department,
        'total_videos': video_lectures.count()
    }
    return render(request, 'TechSutraapp/video_lectures.html', context)

@login_required(login_url='login')
def view(request):
    file_path = request.GET.get('file', '')
    return render(request, 'TechSutraapp/view.html', {'file_path': file_path})

@login_required(login_url='login')
def dashboard(request):
    # Fetch all departments
    departments = Department.objects.all()
    
    # Get URL parameters for direct navigation
    selected_branch = request.GET.get('branch', '')
    selected_semester = request.GET.get('semester', '')
    
    # Build a tree structure for dependent dropdowns
    tree = {}
    for dept in departments:
        tree[dept.name] = {}
        for sem in dept.semesters.all():
            sem_name = f"Semester {sem.number}"
            if sem_name not in tree[dept.name]:
                tree[dept.name][sem_name] = {}
            for sub in sem.subjects.all():
                tree[dept.name][sem_name][sub.name] = sub.id
            
        for sem_name in tree[dept.name]:
            # Convert dictionary back to list of dicts: [{'id': 1, 'name': 'SEPM'}]
            tree[dept.name][sem_name] = [{'id': v, 'name': k} for k, v in tree[dept.name][sem_name].items()]
            
    context = {
        'departments': departments,
        'tree_json': json.dumps(tree),
        'selected_branch': selected_branch,
        'selected_semester': selected_semester,
    }
    return render(request, 'TechSutraapp/dashboard.html', context)

@login_required(login_url='login')
def resources(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    resources = subject.resources.all()
    video_lectures = subject.video_lectures.all()
    
    context = {
        'subject': subject,
        'notes_pdf': resources.filter(file_type='notes_pdf'),
        'notes_ppt': resources.filter(file_type='notes_ppt'),
        'question_papers': resources.filter(file_type='qp'),
        'videos': resources.filter(file_type='video'),
        'video_lectures': video_lectures,
        'syllabus': resources.filter(file_type='syllabus')
    }
    return render(request, 'TechSutraapp/resources.html', context)

@login_required(login_url='login')
def resource_list(request, subject_id, resource_type):
    subject = get_object_or_404(Subject, id=subject_id)
    files = subject.resources.filter(file_type=resource_type)
    
    type_display = {
        'notes_pdf': 'Notes (PDF)',
        'notes_ppt': 'Notes (PPT)',
        'syllabus': 'Syllabus',
        'qp': 'Question Papers'
    }.get(resource_type, 'Resources')

    context = {
        'subject': subject,
        'files': files,
        'resource_type': resource_type,
        'type_display': type_display,
    }
    return render(request, 'TechSutraapp/resource_list.html', context)

def login_view(request):
    if request.method == "POST":
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        if not User.objects.filter(username=username_input).exists():
            messages.error(request, "the username is not available")
        else:
            user = authenticate(request, username=username_input, password=password_input)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password.")
    return render(request, 'TechSutraapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == "POST":
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        if User.objects.filter(username=username_input).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=username_input, password=password_input)
            UserRegistrationData.objects.create(user=user, username=username_input, role='student')
            login(request, user)
            return redirect('dashboard')
    return render(request, 'TechSutraapp/register.html')

def csrf_failure(request, reason=""):
    """
    Custom CSRF failure view that provides helpful information
    """
    return render(request, 'TechSutraapp/csrf_failure.html', {
        'reason': reason,
        'title': 'Security Error'
    })