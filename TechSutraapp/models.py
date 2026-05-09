from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


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
        )],
        blank=True,
        null=True
    )
    video_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="For video resources only: Link to YouTube, Vimeo, or other video platforms"
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        if self.file_type == 'video':
            # For video: either file or URL must be provided
            if not self.video_url and not self.file:
                raise ValidationError('Please provide either a video URL or upload a video file.')
        else:
            # For other resources: file is required
            if not self.file:
                raise ValidationError(f'File is required for {self.get_file_type_display()}.')

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


# ✅ Dedicated Video Lecture linked to Subject (URL-based only)
class VideoLecture(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="video_lectures")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # URL-based videos only (YouTube, Vimeo, etc.)
    video_url = models.URLField(
        default='https://www.youtube.com/watch?v=placeholder',
        help_text="Link to YouTube, Vimeo, or other video platforms (Required)"
    )
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Video URL is required and must not be placeholder
        if not self.video_url or self.video_url == 'https://www.youtube.com/watch?v=placeholder':
            raise ValidationError('Video URL is required. Please provide a valid YouTube, Vimeo, or other video platform URL.')

    def __str__(self):
        return f"{self.title} - {self.subject.name}"
