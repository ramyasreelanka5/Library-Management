"""
Utility Functions and Decorators
Helper functions for permission checks, notifications, and common operations
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Notification, AuditLog


def role_required(allowed_roles):
    """
    Decorator to check if user has required role
    Usage: @role_required(['ADMIN', 'LIBRARIAN'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'profile'):
                user_role = request.user.profile.role
                if user_role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        
        return wrapped_view
    return decorator


def admin_required(view_func):
    """Decorator for admin-only views"""
    return role_required(['ADMIN'])(view_func)


def librarian_required(view_func):
    """Decorator for admin and librarian views"""
    return role_required(['ADMIN', 'LIBRARIAN'])(view_func)


def student_required(view_func):
    """Decorator for student views"""
    return role_required(['STUDENT'])(view_func)


def create_notification(user, notification_type, title, message, related_issue=None, related_reservation=None):
    """Create a notification for a user"""
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_issue=related_issue,
        related_reservation=related_reservation
    )


def log_audit(user, action, model_name, object_id=None, description='', request=None):
    """Log an audit entry"""
    ip_address = None
    user_agent = ''
    
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent
    )


def get_user_role(user):
    """Get user's role"""
    if hasattr(user, 'profile'):
        return user.profile.role
    return None


def is_admin(user):
    """Check if user is admin"""
    return get_user_role(user) == 'ADMIN'


def is_librarian(user):
    """Check if user is admin or librarian"""
    role = get_user_role(user)
    return role in ['ADMIN', 'LIBRARIAN']


def is_student(user):
    """Check if user is student"""
    return get_user_role(user) == 'STUDENT'
