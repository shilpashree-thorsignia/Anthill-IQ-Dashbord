from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import requests
import os
import json
from django.conf import settings
from django.core.cache import cache
from django.db import OperationalError, connection, connections
from django.db.models import Count, Avg
import time
import logging
from psycopg2 import OperationalError as Psycopg2OperationalError
from .models import User, Conversation

logger = logging.getLogger(__name__)

def get_railway_api_headers():
    return {
        'Authorization': f'Bearer {os.getenv("RAILWAYAPI")}',
        'Content-Type': 'application/json'
    }

def fetch_railway_data(query, cache_key=None, cache_timeout=600):
    """
    Fetch data from Railway API with caching support and retry mechanism
    """
    if cache_key:
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

    max_retries = 5
    retry_delay = 2
    max_delay = 30

    for attempt in range(max_retries):
        try:
            response = requests.post(
                'https://backboard.railway.app/graphql/v2',
                headers=get_railway_api_headers(),
                json={'query': query},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if cache_key:
                cache.set(cache_key, data, cache_timeout)
            
            return data
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                delay = min(retry_delay * (2 ** attempt), max_delay)
                time.sleep(delay)
            continue
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error on attempt {attempt + 1}/{max_retries}: {str(e)}")
            if attempt < max_retries - 1:
                delay = min(retry_delay * (2 ** attempt), max_delay)
                time.sleep(delay)
            continue
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}/{max_retries}: {str(e)}")
            if attempt < max_retries - 1:
                delay = min(retry_delay * (2 ** attempt), max_delay)
                time.sleep(delay)
            continue
    
    return None

def get_default_dashboard_context():
    """Return default context when data can't be fetched"""
    return {
        'total_users': 0,
        'total_conversations': 0,
        'total_messages': 0,
        'active_users': 0,
        'message_chart': '',
        'recent_conversations': [],
        'refresh_interval': 600000,  # 10 minutes in milliseconds
        'error': 'Unable to fetch data. Using cached data if available.',
    }

@login_required
def dashboard(request):
    try:
        # Get total users
        total_users = User.objects.using('railway').count()
        
        # Get total conversations
        total_conversations = Conversation.objects.using('railway').count()
        
        # Get active users in last 24 hours (users who have had activity in last 24h)
        last_24h = timezone.now() - timedelta(hours=24)
        active_users = User.objects.using('railway').filter(
            timestamp__gte=last_24h
        ).distinct('session_id').count()
        
        # Get total messages
        total_messages = Conversation.objects.using('railway').filter(
            user_message__isnull=False
        ).count() + Conversation.objects.using('railway').filter(
            bot_response__isnull=False
        ).count()
        
        # Get recent conversations with user details using ORM
        recent_conversations = Conversation.objects.using('railway').select_related(
            'user'
        ).order_by('-timestamp')[:10]
        
        # Get all users for display, excluding those with empty session_ids
        users = User.objects.using('railway').exclude(
            session_id__isnull=True
        ).exclude(
            session_id=''
        ).order_by('-timestamp')
        
        context = {
            'total_users': total_users,
            'total_conversations': total_conversations,
            'active_users': active_users,
            'total_messages': total_messages,
            'recent_conversations': recent_conversations,
            'users': users,
            'refresh_interval': 600000,  # 10 minutes in milliseconds
        }
        
        return render(request, 'analytics/dashboard.html', context)
        
    except Exception as e:
        logger.error(f"Error loading dashboard data: {str(e)}")
        context = {
            'error': f"Error loading dashboard data: {str(e)}",
            'total_users': 0,
            'total_conversations': 0,
            'active_users': 0,
            'total_messages': 0,
            'recent_conversations': [],
            'users': [],
            'refresh_interval': 600000,  # 10 minutes in milliseconds
        }
        return render(request, 'analytics/dashboard.html', context)

@login_required
def user_detail(request, user_id):
    try:
        cache_key = f'user_detail_{user_id}'
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            # Get specific user details
            user = User.objects.using('railway').filter(session_id=user_id).first()
            if not user:
                raise Exception(f"User with session ID {user_id} not found")
            
            logger.info(f"Found user: {user.session_id}")
            
            # Get user's conversations with pagination
            conv_page = request.GET.get('conv_page', 1)
            try:
                conv_page = int(conv_page)
            except ValueError:
                conv_page = 1
            
            per_page = 10
            conv_offset = (conv_page - 1) * per_page
            
            # Get conversations using ORM with proper filtering
            conversations = Conversation.objects.using('railway').filter(
                user__session_id=user_id  # Filter by session_id
            ).order_by('-timestamp')
            
            total_conversations = conversations.count()
            logger.info(f"Total conversations found: {total_conversations}")
            
            # Apply pagination
            conversations = conversations[conv_offset:conv_offset + per_page]
            logger.info(f"Retrieved {len(conversations)} conversations for page {conv_page}")
            
            context = {
                'user': user,
                'conversations': conversations,
                'conv_pagination': {
                    'current_page': conv_page,
                    'total_pages': (total_conversations + per_page - 1) // per_page,
                    'has_next': conv_page * per_page < total_conversations,
                    'has_previous': conv_page > 1
                }
            }
            
            # Cache the context
            cache.set(cache_key, context, 600)  # Cache for 10 minutes
        else:
            context = cached_data
        
    except Exception as e:
        logger.error(f"Error in user_detail view: {str(e)}")
        context = {'error': f'An error occurred: {str(e)}'}
        if cached_data:  # Use old cached data if available
            context.update(cached_data)
    
    return render(request, 'analytics/user_detail.html', context)

@login_required
def conversation_detail(request, conversation_id):
    try:
        cache_key = f'conversation_detail_{conversation_id}'
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            # Get all conversations with this ID
            conversations = Conversation.objects.using('railway').select_related(
                'user'
            ).filter(id=conversation_id).order_by('-timestamp')
            
            if not conversations.exists():
                raise Exception(f"Conversation with ID {conversation_id} not found")
            
            # Get the first conversation to get user info
            first_conversation = conversations.first()
            
            # Get all conversations for this user
            user_conversations = Conversation.objects.using('railway').filter(
                user__session_id=first_conversation.user.session_id
            ).order_by('-timestamp')
            
            # Get the current conversation's position in the list
            conversation_list = list(user_conversations)
            current_index = next((i for i, c in enumerate(conversation_list) if c.id == conversation_id), 0)
            
            context = {
                'conversations': conversations,  # All conversations with this ID
                'current_conversation': first_conversation,  # The first conversation for display
                'user_conversations': user_conversations,  # All conversations for this user
                'total_conversations': user_conversations.count(),
                'current_index': current_index,
                'has_previous': current_index < len(conversation_list) - 1,
                'has_next': current_index > 0,
                'previous_conversation': conversation_list[current_index + 1] if current_index < len(conversation_list) - 1 else None,
                'next_conversation': conversation_list[current_index - 1] if current_index > 0 else None,
                'multiple_conversations': conversations.count() > 1,  # Flag to indicate multiple conversations
            }
            
            # Cache the context
            cache.set(cache_key, context, 600)  # Cache for 10 minutes
        else:
            context = cached_data
        
    except Exception as e:
        logger.error(f"Error in conversation_detail view: {str(e)}")
        context = {'error': f'An error occurred: {str(e)}'}
        if cached_data:  # Use old cached data if available
            context.update(cached_data)
    
    return render(request, 'analytics/conversation_detail.html', context)

def testuser(request):
    total_users = User.objects.all()
    return render(request, 'testuser.html', {'total_users': total_users})
