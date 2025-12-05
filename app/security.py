import bleach

def sanitize_html(text):
    """
    Sanitize HTML content to prevent XSS attacks.
    Allows only safe tags and attributes.
    """
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'code', 'pre']
    allowed_attributes = {'a': ['href', 'title']}
    
    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )

def validate_password(password):
    """
    Validate password strength.
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, 'La contraseña debe tener al menos 8 caracteres.'
    
    if not any(c.isupper() for c in password):
        return False, 'La contraseña debe contener al menos una letra mayúscula.'
    
    if not any(c.isdigit() for c in password):
        return False, 'La contraseña debe contener al menos un número.'
    
    return True, None

def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension.
    Returns True if extension is allowed, False otherwise.
    """
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions
