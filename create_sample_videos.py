import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechSutraproj.settings')
django.setup()

from TechSutraapp.models import Department, Semester, Subject, VideoLecture, User

# Create sample video lectures if they don't exist
def create_sample_videos():
    try:
        # Get first admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("No admin user found. Please create an admin user first.")
            return

        # Get first subject
        subject = Subject.objects.first()
        if not subject:
            print("No subjects found. Please add subjects first.")
            return

        # Sample video URLs
        sample_videos = [
            {
                'title': 'Introduction to Python Programming',
                'description': 'Learn the basics of Python programming language',
                'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8'
            },
            {
                'title': 'Django Web Framework Tutorial',
                'description': 'Complete guide to building web applications with Django',
                'video_url': 'https://www.youtube.com/watch?v=F5mRW0jo-U4'
            },
            {
                'title': 'Database Management Systems Overview',
                'description': 'Understanding relational databases and SQL',
                'video_url': 'https://www.youtube.com/watch?v=FR4QIeZaPeM'
            }
        ]

        for video_data in sample_videos:
            if not VideoLecture.objects.filter(title=video_data['title']).exists():
                VideoLecture.objects.create(
                    subject=subject,
                    uploaded_by=admin_user,
                    **video_data
                )
                print(f"Created video lecture: {video_data['title']}")
            else:
                print(f"Video lecture already exists: {video_data['title']}")

        print(f"Total video lectures: {VideoLecture.objects.count()}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_sample_videos()