from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from .models import User as CustomUser, Conversation
from django.utils import timezone
from django.urls import reverse
from unittest import mock
from django.db import connections

# Create your tests here.

@override_settings(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
class PhoneNumberDisplayTest(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        
        # Create test data
        self.test_users = [
            {
                'session_id': 'test1',
                'name': 'Test User 1',
                'phone': '1234567890',
                'email': 'test1@example.com',
                'source': 'test',
                'timestamp': timezone.now()
            },
            {
                'session_id': 'test2',
                'name': 'Test User 2',
                'phone': '',
                'email': 'test2@example.com',
                'source': 'test',
                'timestamp': timezone.now()
            },
            {
                'session_id': 'test3',
                'name': 'Test User 3',
                'phone': None,
                'email': 'test3@example.com',
                'source': 'test',
                'timestamp': timezone.now()
            }
        ]

        # Mock the User model's using().count() method
        self.user_count_patcher = mock.patch.object(CustomUser.objects.using('railway'), 'count')
        self.mock_user_count = self.user_count_patcher.start()
        self.mock_user_count.return_value = len(self.test_users)

        # Mock the Conversation model's using().count() method
        self.conv_count_patcher = mock.patch.object(Conversation.objects.using('railway'), 'count')
        self.mock_conv_count = self.conv_count_patcher.start()
        self.mock_conv_count.return_value = 10

        # Mock the cursor for raw SQL queries
        self.cursor_patcher = mock.patch('django.db.connections')
        self.mock_connections = self.cursor_patcher.start()
        self.mock_cursor = mock.MagicMock()
        self.mock_connection = mock.MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_connections.__getitem__.return_value = self.mock_connection

    def tearDown(self):
        self.user_count_patcher.stop()
        self.conv_count_patcher.stop()
        self.cursor_patcher.stop()

    def test_phone_number_display(self):
        # Set up the mock cursor for user detail
        self.mock_cursor.fetchall.return_value = [
            (user['timestamp'], user['name'], user['phone'], user['email'], user['source'], user['session_id'])
            for user in self.test_users
        ]
        self.mock_cursor.fetchone.return_value = (
            self.test_users[0]['timestamp'],
            self.test_users[0]['name'],
            self.test_users[0]['phone'],
            self.test_users[0]['email'],
            self.test_users[0]['source'],
            self.test_users[0]['session_id']
        )

        # Test user detail view for each user
        for user in self.test_users:
            response = self.client.get(reverse('user_detail', args=[user['session_id']]))
            self.assertEqual(response.status_code, 200)
            
            # Check if phone number is displayed correctly
            if user['phone']:
                self.assertContains(response, user['phone'])
            else:
                self.assertContains(response, 'N/A')

    def test_phone_number_in_recent_conversations(self):
        # Mock conversations data
        test_conversations = [
            {
                'id': 1,
                'user_id': user['session_id'],
                'timestamp': timezone.now(),
                'source': 'test',
                'user_message': 'Test message',
                'bot_response': 'Test response',
                'name': user['name'],
                'phone': user['phone'],
                'email': user['email']
            }
            for user in self.test_users
        ]

        # Update cursor mock for conversations
        self.mock_cursor.fetchall.return_value = [
            (conv['id'], conv['user_id'], conv['timestamp'], conv['source'], 
             conv['user_message'], conv['bot_response'], conv['name'], 
             conv['phone'], conv['email'])
            for conv in test_conversations
        ]

        # Test dashboard view
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check if phone numbers are displayed correctly in recent conversations
        for conv in test_conversations:
            if conv['phone']:
                self.assertContains(response, conv['phone'])
            else:
                self.assertContains(response, 'N/A')
