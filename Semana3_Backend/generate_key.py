"""
Script para Generar Clave AES
"""
import os
import base64


def generate_aes_key():
    """Generar clave AES-256 (32 bytes)"""
    key = os.urandom(32)
    key_b64 = base64.b64encode(key).decode('utf-8')
    
    print("🔑 Clave AES-256 generada exitosamente")
    print("\nAgrega esta línea a tu archivo .env:")
    print(f"\nAES_MASTER_KEY={key_b64}")
    print("\n⚠️  IMPORTANTE: Guarda esta clave de forma segura. Si la pierdes, no podrás descifrar los datos.")


if __name__ == '__main__':
    generate_aes_key()
