from app import db
from app.models import AuditLog
from flask import request
from flask_login import current_user
from datetime import datetime

def log_audit(action, details=None, user_id=None):
    """
    Log an audit event to the database.
    
    Args:
        action (str): A short string describing the action (e.g., 'user_login', 'ticket_created')
        details (str, optional): Additional details about the action.
        user_id (int, optional): The ID of the user performing the action. 
                                 Defaults to current_user.id if available.
    """
    try:
        # Determine user_id
        if user_id is None:
            if current_user and current_user.is_authenticated:
                user_id = current_user.id
            else:
                user_id = 0 # System or Anonymous
                
        # Get IP address
        ip_address = request.remote_addr if request else None
        
        # Create log entry
        log = AuditLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address,
            timestamp=datetime.utcnow()
        )
        
        db.session.add(log)
        db.session.commit()
        print(f"AUDIT LOG: {action} - {details}")
    except Exception as e:
        print(f"FAILED TO LOG AUDIT: {e}")
        db.session.rollback()
