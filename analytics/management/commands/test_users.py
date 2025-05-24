from django.core.management.base import BaseCommand
from analytics.models import User
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test user fetching from the database'

    def handle(self, *args, **options):
        try:
            # Test 1: Get total count
            total_users = User.objects.using('railway').count()
            self.stdout.write(self.style.SUCCESS(f"Total users in database: {total_users}"))
            
            # Test 2: Get all users
            users = User.objects.using('railway').order_by('-timestamp')
            self.stdout.write(self.style.SUCCESS(f"Number of users fetched: {users.count()}"))
            
            # Test 3: Print first 5 users
            self.stdout.write("\nFirst 5 users:")
            for i, user in enumerate(users[:5], 1):
                self.stdout.write(f"User {i}:")
                self.stdout.write(f"  Session ID: {user.session_id}")
                self.stdout.write(f"  Name: {user.name or 'Unknown'}")
                self.stdout.write(f"  Phone: {user.phone or 'N/A'}")
                self.stdout.write(f"  Timestamp: {user.timestamp}")
                self.stdout.write("---")
            
            # Summary
            self.stdout.write("\nSummary:")
            self.stdout.write(f"Total users in database: {total_users}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}")) 