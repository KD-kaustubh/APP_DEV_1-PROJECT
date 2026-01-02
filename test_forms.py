#!/usr/bin/env python
"""Test script to verify forms are working with WTForms"""

import requests
import re
from requests.adapters import HTTPAdapter

# Create a session
session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))

BASE_URL = 'http://127.0.0.1:5000'

# Step 1: Login
print("[1] Logging in...")
login_response = session.post(f'{BASE_URL}/login', data={
    'username': 'admin@gmail.com',
    'password': 'Admin123',
}, allow_redirects=False)
print(f"    Login response: {login_response.status_code}")

# Step 2: Get the add_subjects form page
print("[2] Getting add_subjects form...")
form_response = session.get(f'{BASE_URL}/add_subjects')
print(f"    Form response: {form_response.status_code}")

# Extract CSRF token
csrf_match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', form_response.text)
if csrf_match:
    csrf_token = csrf_match.group(1)
    print(f"    CSRF token found: {csrf_token[:20]}...")
else:
    print("    ERROR: CSRF token not found!")
    # Print a sample of the form
    form_sample = form_response.text[form_response.text.find('csrf'):form_response.text.find('csrf')+200]
    print(f"    Form sample: {form_sample}")

# Step 3: Submit the form
print("[3] Submitting form...")
submit_response = session.post(f'{BASE_URL}/add_subjects', data={
    'csrf_token': csrf_token,
    'name': 'Test Subject',
    'description': 'Test Description'
}, allow_redirects=False)

print(f"    Submit response: {submit_response.status_code}")
if submit_response.status_code == 302:
    print("    ✓ SUCCESS: Form submitted with 302 redirect!")
    redirect_location = submit_response.headers.get('Location', 'N/A')
    print(f"    Redirected to: {redirect_location}")
elif submit_response.status_code == 200:
    print("    ✗ FAILED: Form returned 200 (no redirect)")
    # Check for error messages
    if 'error' in submit_response.text.lower():
        print("    Error found in response")
    if 'alert' in submit_response.text.lower():
        print("    Alert found in response")
else:
    print(f"    ? Unexpected status: {submit_response.status_code}")

print("\n[Done]")
