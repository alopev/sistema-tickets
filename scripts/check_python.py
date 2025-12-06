#!/usr/bin/env python
"""
Script para verificar la arquitectura de Python (32-bit vs 64-bit)
y advertir sobre limitaciones de pandas en Python 32-bit.
"""
import sys
import struct

def check_python_architecture():
    """Verifica si Python es 64-bit y muestra advertencias si es necesario"""
    bits = struct.calcsize('P') * 8
    version = sys.version_info
    
    print("="*60)
    print("🐍 VERIFICACIÓN DE PYTHON")
    print("="*60)
    print(f"\n📌 Versión: Python {version.major}.{version.minor}.{version.micro}")
    print(f"📌 Arquitectura: {bits}-bit")
    print(f"📌 Ejecutable: {sys.executable}")
    print()
    
    if bits == 32:
        print("⚠️  WARNING: Estás usando Python de 32 bits")
        print("="*60)
        print("\nAlgunas características estarán limitadas:")
        print("  ❌ Exportación a Excel/CSV (pandas) puede fallar al instalarse")
        print("  ❌ Rendimiento reducido en procesamiento de datos")
        print()
        print("💡 RECOMENDACIÓN:")
        print("  Instala Python 64-bit para acceso completo a todas las funciones.")
        print()
        print("📥 Descarga Python 64-bit desde:")
        print("  https://www.python.org/downloads/")
        print()
        print("  Busca: 'Windows installer (64-bit)'")
        print("="*60)
        return False
    else:
        print("✅ Python 64-bit detectado")
        print("="*60)
        print("\n🎉 Todas las características estarán disponibles:")
        print("  ✅ Exportación a Excel/CSV (pandas)")
        print("  ✅ Procesamiento óptimo de datos")
        print("  ✅ Todas las librerías sin restricciones")
        print("="*60)
        return True

if __name__ == "__main__":
    is_64bit = check_python_architecture()
    sys.exit(0 if is_64bit else 1)
