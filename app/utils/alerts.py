"""
Centralized alert system for consistent user notifications.
Uses session storage to pass alerts to the frontend for SweetAlert2 rendering.
"""
from flask import session

def _add_alert(message, category):
    """Internal function to add alerts to session."""
    if 'alerts' not in session:
        session['alerts'] = []
    session['alerts'].append({
        'message': message,
        'category': category
    })

def success(message):
    """Add a success alert (green checkmark)."""
    _add_alert(message, 'success')

def error(message):
    """Add an error alert (red X)."""
    _add_alert(message, 'error')

def warning(message):
    """Add a warning alert (yellow exclamation)."""
    _add_alert(message, 'warning')

def info(message):
    """Add an info alert (blue i)."""
    _add_alert(message, 'info')

def get_alerts():
    """Get all pending alerts and clear them from session."""
    alerts = session.pop('alerts', [])
    return alerts
