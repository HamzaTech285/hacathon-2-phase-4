#!/usr/bin/env python3
"""
Basic API security test script for the Todo App backend.
This script tests that authenticated API calls succeed and unauthenticated calls fail appropriately.
"""

import requests
import json
import os
from typing import Optional

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def test_unauthenticated_access():
    """Test that unauthenticated requests to task endpoints fail with 401."""
    print("Testing unauthenticated access to task endpoints...")

    # Try to access tasks without authentication
    try:
        response = requests.get(f"{BASE_URL}/api/tasks")
        print(f"GET /api/tasks - Status: {response.status_code} (Expected: 401)")

        if response.status_code == 401:
            print("✓ Unauthenticated access correctly denied")
        else:
            print("✗ Unauthenticated access incorrectly allowed")

    except Exception as e:
        print(f"Error testing unauthenticated access: {e}")

def test_auth_endpoints():
    """Test that authentication endpoints are accessible without auth."""
    print("\nTesting authentication endpoints...")

    # Try to access the health check endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"GET /health - Status: {response.status_code} (Expected: 200)")

        if response.status_code == 200:
            print("✓ Health check endpoint accessible")
        else:
            print("✗ Health check endpoint not accessible")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")

    # Try to access the root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"GET / - Status: {response.status_code} (Expected: 200)")

        if response.status_code == 200:
            print("✓ Root endpoint accessible")
        else:
            print("✗ Root endpoint not accessible")
    except Exception as e:
        print(f"Error testing root endpoint: {e}")

def test_basic_authentication_flow():
    """Test the basic authentication flow with a temporary user."""
    print("\nTesting basic authentication flow...")

    # Create a test user
    test_email = "testuser@example.com"
    test_password = "securepassword123"

    auth_data = {
        "email": test_email,
        "password": test_password
    }

    try:
        # Try to register the user
        print(f"Attempting to register user: {test_email}")
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=auth_data)
        print(f"POST /api/auth/signup - Status: {response.status_code}")

        if response.status_code in [200, 400]:  # 400 might mean user already exists
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                print("✓ User registration successful or user already exists")

                # Try to access tasks with the token
                if token:
                    headers = {"Authorization": f"Bearer {token}"}
                    task_response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
                    print(f"GET /api/tasks with valid token - Status: {task_response.status_code} (Expected: 200)")

                    if task_response.status_code == 200:
                        print("✓ Authenticated access to tasks successful")
                    else:
                        print("✗ Authenticated access to tasks failed")
            else:
                print("Note: User may already exist")
        else:
            print(f"✗ Registration failed with status: {response.status_code}")

    except Exception as e:
        print(f"Error testing authentication flow: {e}")

def main():
    print("Starting API Security Tests...\n")

    test_auth_endpoints()
    test_unauthenticated_access()
    test_basic_authentication_flow()

    print("\nAPI Security Tests Complete!")

if __name__ == "__main__":
    main()