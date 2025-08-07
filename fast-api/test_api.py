#!/usr/bin/env python3
"""
Simple test script to verify API functionality
"""

import json

import requests

BASE_URL = "http://localhost:8000"


def test_signup():
    """Test user signup"""
    print("Testing /signup endpoint...")

    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/signup", json=user_data)

    if response.status_code == 200:
        print("✅ Signup successful!")
        return user_data
    else:
        print(f"❌ Signup failed: {response.status_code} - {response.text}")
        return None


def test_login(user_data):
    """Test user login and get JWT token"""
    print("\nTesting /token endpoint...")

    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }

    response = requests.post(f"{BASE_URL}/token", data=login_data)

    if response.status_code == 200:
        token_data = response.json()
        print("✅ Login successful!")
        print(f"Token: {token_data['access_token'][:50]}...")
        return token_data["access_token"]
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None


def test_random_endpoint():
    """Test the /random endpoint"""
    print("\nTesting /random endpoint...")

    response = requests.get(f"{BASE_URL}/random")

    if response.status_code == 200:
        data = response.json()
        print("✅ Random endpoint successful!")
        print(f"Random number: {data['random_number']}")
        print(f"Selected user: {data['user']['name']} ({data['user']['email']})")
        print(f"Number of posts: {len(data['posts'])}")
        print(f"JWT token: {data['jwt_token'][:50]}...")
        return data
    else:
        print(f"❌ Random endpoint failed: {response.status_code} - {response.text}")
        return None


def test_protected_endpoint(token):
    """Test protected endpoint with JWT token"""
    print("\nTesting protected endpoint /users/me...")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        print("✅ Protected endpoint successful!")
        print(f"User: {user_data['name']} ({user_data['email']})")
    else:
        print(f"❌ Protected endpoint failed: {response.status_code} - {response.text}")


def main():
    """Run all tests"""
    print("🚀 Starting API tests...\n")

    # Test signup
    user_data = test_signup()
    if not user_data:
        print("Skipping remaining tests due to signup failure.")
        return

    # Test login
    token = test_login(user_data)
    if not token:
        print("Skipping remaining tests due to login failure.")
        return

    # Test random endpoint
    random_data = test_random_endpoint()
    if not random_data:
        print("Random endpoint test failed.")
        return

    # Test protected endpoint with the token from random endpoint
    test_protected_endpoint(random_data['jwt_token'])

    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    main()
