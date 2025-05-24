from django.core.management.base import BaseCommand
from analytics.models import User, Conversation
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the conversations table with test data'

    def handle(self, *args, **kwargs):
        # Get all users
        users = User.objects.using('railway').all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found in the database'))
            return
        
        # Sample messages for testing
        user_messages = [
            "Hello, how can you help me?",
            "What services do you offer?",
            "I need information about your products",
            "Can you tell me more about your company?",
            "How do I get started?",
            "What are your business hours?",
            "Do you have any special offers?",
            "I have a question about my account",
            "Can you help me with a problem?",
            "What are your contact details?"
        ]
        
        bot_responses = [
            "Hello! I'm here to help you with any questions you have.",
            "We offer a wide range of services. What are you interested in?",
            "I'd be happy to tell you about our products. What would you like to know?",
            "Our company specializes in providing excellent service to our customers.",
            "Getting started is easy! Let me guide you through the process.",
            "We're open Monday through Friday, 9 AM to 5 PM.",
            "Yes, we have several special offers available right now!",
            "I can help you with your account. What do you need to know?",
            "I'll do my best to help you solve your problem.",
            "You can reach us at support@example.com or call 123-456-7890."
        ]
        
        # Create conversations for each user
        for user in users:
            # Create 2-5 conversations per user
            num_conversations = random.randint(2, 5)
            
            for i in range(num_conversations):
                # Create a conversation with random message and response
                conversation = Conversation.objects.using('railway').create(
                    user=user,
                    user_message=random.choice(user_messages),
                    bot_response=random.choice(bot_responses),
                    source='test_data',
                    timestamp=timezone.now()
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created conversation {conversation.id} for user {user.session_id}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated conversations')) 