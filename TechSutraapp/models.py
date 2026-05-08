from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator


# ✅ Department (same as Branch)
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ Semester linked to Department
class Semester(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="semesters")
    number = models.IntegerField()

    def __str__(self):
        return f"{self.department.name} - Sem {self.number}"


# ✅ Subject linked to Semester
class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.semester})"


RESOURCE_TYPES = (
    ('notes_pdf', 'Notes (PDF)'),
    ('notes_ppt', 'Notes (PPT)'),
    ('syllabus', 'Syllabus'),
    ('qp', 'Question Paper'),
    ('video', 'Video Lecture'),
)

# ✅ Resource linked to Subject
class Resource(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    file_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='notes_pdf')
    file = models.FileField(
        upload_to='resources/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'mp4', 'webm', 'ogg']
        )]
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.get_file_type_display()})"


# ✅ User Extra Data
class UserRegistrationData(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='registration_data'
    )
    username = models.CharField(max_length=150)
    registered_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('teacher', 'Teacher'),
            ('admin', 'Admin')
        ],
        default='student'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "User Registration Data"
        verbose_name_plural = "User Registration Data"

# ✅ Global Platform Review
class PlatformReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Platform Review by {self.user.username}"


# ✅ Dedicated Video Lecture linked to Subject
class VideoLecture(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="video_lectures")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Support for both file uploads and external URLs 
    video_file = models.FileField(
        upload_to='video_lectures/', 
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg', 'mkv'])],
        blank=True, 
        null=True
    )
    video_url = models.URLField(blank=True, null=True, help_text="Link to YouTube or external video")
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name}"
