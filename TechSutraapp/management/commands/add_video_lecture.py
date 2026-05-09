from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from TechSutraapp.models import VideoLecture, Subject


class Command(BaseCommand):
    help = 'Add a video lecture to a subject via URL (Admin only)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--subject-id',
            type=int,
            required=True,
            help='ID of the subject to add the video to'
        )
        parser.add_argument(
            '--title',
            type=str,
            required=True,
            help='Title of the video lecture'
        )
        parser.add_argument(
            '--url',
            type=str,
            required=True,
            help='URL of the video (YouTube, Vimeo, or other platforms)'
        )
        parser.add_argument(
            '--description',
            type=str,
            required=False,
            default='',
            help='Description of the video lecture'
        )
        parser.add_argument(
            '--uploaded-by-id',
            type=int,
            required=False,
            help='User ID of the admin uploading the video (default: superuser)'
        )

    def handle(self, *args, **options):
        try:
            # Get the subject
            subject = Subject.objects.get(id=options['subject_id'])
        except Subject.DoesNotExist:
            raise CommandError(f"Subject with ID {options['subject_id']} does not exist")

        # Get the user (admin) who is uploading
        if options['uploaded_by_id']:
            try:
                user = User.objects.get(id=options['uploaded_by_id'])
            except User.DoesNotExist:
                raise CommandError(f"User with ID {options['uploaded_by_id']} does not exist")
        else:
            # Use the first superuser if no user is specified
            try:
                user = User.objects.filter(is_superuser=True).first()
                if not user:
                    raise CommandError("No admin user found. Please specify --uploaded-by-id")
            except User.DoesNotExist:
                raise CommandError("No admin user found. Please specify --uploaded-by-id")

        # Create the video lecture
        try:
            video_lecture = VideoLecture.objects.create(
                subject=subject,
                title=options['title'],
                description=options['description'],
                video_url=options['url'],
                uploaded_by=user
            )
            video_lecture.full_clean()  # Validate before saving
            video_lecture.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Video lecture "{video_lecture.title}" successfully added to '
                    f'subject "{subject.name}"'
                )
            )
        except Exception as e:
            raise CommandError(f'Failed to add video lecture: {str(e)}')
