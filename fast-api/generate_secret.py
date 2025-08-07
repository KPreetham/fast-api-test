#!/usr/bin/env python3
"""
Utility script to generate secure JWT secret keys
"""

import secrets
import string


def generate_jwt_secret(length: int = 32) -> str:
    """
    Generate a secure JWT secret key

    Args:
        length: Length of the secret key (default: 32)

    Returns:
        A secure random string suitable for JWT signing
    """
    # Use URL-safe base64 encoding for better compatibility
    return secrets.token_urlsafe(length)


def generate_database_password(length: int = 16) -> str:
    """
    Generate a secure database password

    Args:
        length: Length of the password (default: 16)

    Returns:
        A secure random password
    """
    # Use a mix of letters, digits, and special characters
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))


def main():
    """Generate and display secure credentials"""
    print("🔐 Secure Credentials Generator")
    print("=" * 40)

    # Generate JWT secret
    jwt_secret = generate_jwt_secret()
    print(f"\nJWT Secret Key:")
    print(f"JWT_SECRET_KEY={jwt_secret}")

    # Generate database password
    db_password = generate_database_password()
    print(f"\nDatabase Password:")
    print(f"DB_PASSWORD={db_password}")

    # Show example DATABASE_URL
    print(f"\nExample DATABASE_URL:")
    print(f"DATABASE_URL=postgresql://username:{db_password}@localhost:5432/fastapi_demo")

    print(f"\n📝 Copy these values to your .env file!")
    print(f"⚠️  Keep these secrets secure and never commit them to version control!")


if __name__ == "__main__":
    main()
