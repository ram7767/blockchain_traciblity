"""
Custom decorators for role-based access control.
Uses session-based authentication with UserProfile model.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def login_required_custom(view_func):
    """Require user to be logged in via session."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(role):
    """Require user to have a specific role."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'user_id' not in request.session:
                messages.error(request, 'Please login to access this page.')
                return redirect('login')
            if request.session.get('user_type') != role:
                messages.error(request, f'Access denied. {role} role required.')
                return redirect('index')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """Require Admin role."""
    return role_required('Admin')(view_func)


def farmer_required(view_func):
    """Require Farmer role."""
    return role_required('Farmer')(view_func)


def consumer_required(view_func):
    """Require Consumer role."""
    return role_required('Consumer')(view_func)
