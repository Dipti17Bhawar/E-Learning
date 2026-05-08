import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechSutraproj.settings')
django.setup()

from TechSutraapp.models import Resource
deleted, _ = Resource.objects.filter(file='').delete()
print(f"Deleted {deleted} resources with empty files.")
