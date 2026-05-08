from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from TechSutraapp.models import UserRegistrationData

class Command(BaseCommand):
    help = 'Promote a user to teacher or admin role'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to promote')
        parser.add_argument('role', type=str, choices=['teacher', 'admin'], help='Role to assign')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        
        try:
            user = User.objects.get(username=username)
            reg_data, created = UserRegistrationData.objects.get_or_create(
                user=user,
                defaults={'username': username, 'role': role}
            )
            if not created:
                reg_data.role = role
                reg_data.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully promoted {username} to {role}')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} does not exist')
            )