from django.core.management.base import BaseCommand
from chat.models import UserProfile
from django.contrib.auth.models import User
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Create user profiles for existing users without profiles'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(userprofile__isnull=True)

        # Set the path to your default profile picture
        default_image_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', 'default_profile_picture.jpg')

        for user in users_without_profiles:
            # Create a UserProfile for the user
            user_profile = UserProfile(user=user)

            # Add the default profile picture
            with open(default_image_path, 'rb') as image_file:
                user_profile.profile_picture.save('default_profile_picture.jpg', File(image_file), save=True)

            user_profile.save()
            self.stdout.write(self.style.SUCCESS(f'Created profile for user {user.username}'))
