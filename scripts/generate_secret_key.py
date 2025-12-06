#!/usr/bin/env python
"""
Script para generar una SECRET_KEY aleatoria y segura para Flask.
"""
import secrets
import string

def generate_secret_key(length=50):
    """
    Genera una clave secreta segura para Flask usando caracteres aleatorios.
    
    Args:
        length (int): Longitud de la clave a generar (default: 50)
        
    Returns:
        str: Clave secreta aleatoria
    """
    # Usar una combinación de letras, dígitos y algunos caracteres especiales seguros
    alphabet = string.ascii_letters + string.digits + '-_!@#$%^&*()'
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

if __name__ == "__main__":
    print("="*60)
    print("🔐 GENERADOR DE SECRET_KEY")
    print("="*60)
    print()
    
    key = generate_secret_key()
    
    print("✅ SECRET_KEY generada exitosamente:")
    print()
    print("-"*60)
    print(f"SECRET_KEY={key}")
    print("-"*60)
    print()
    print("📋 INSTRUCCIONES:")
    print("  1. Copia la línea completa de arriba (SECRET_KEY=...)")
    print("  2. Abre tu archivo .env")
    print("  3. Reemplaza la línea SECRET_KEY existente")
    print("  4. Guarda el archivo")
    print()
    print("⚠️  IMPORTANTE: Mantén esta clave en secreto y no la compartas.")
    print("="*60)
