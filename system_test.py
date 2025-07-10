#!/usr/bin/env python3
"""
Comprehensive system test for the Forensic AI Tool
Tests all major components and endpoints
"""

import requests
import json
import os
import tempfile
import time
from pathlib import Path

BASE_URL = "http://localhost:12000"

def test_status_endpoints():
    """Test system status endpoints"""
    print("🔍 Testing status endpoints...")
    
    # Test main status
    response = requests.get(f"{BASE_URL}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("✅ Main status endpoint working")
    
    # Test utility status
    response = requests.get(f"{BASE_URL}/util-status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("✅ Utility status endpoint working")

def test_voice_command():
    """Test voice command processing"""
    print("🎤 Testing voice command endpoint...")
    
    test_commands = [
        "check system status",
        "analyze permissions",
        "run security scan"
    ]
    
    for command in test_commands:
        response = requests.post(
            f"{BASE_URL}/voice-command",
            json={"transcript": command}
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert command in data["response"]
        print(f"✅ Voice command processed: {command}")

def test_web_scraper():
    """Test web scraping functionality"""
    print("🕷️ Testing web scraper endpoint...")
    
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html"
    ]
    
    for url in test_urls:
        response = requests.post(
            f"{BASE_URL}/scrape-website",
            json={"url": url}
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "file_links" in data
        print(f"✅ Web scraper tested with: {url}")

def test_apk_analysis():
    """Test APK analysis functionality (mock)"""
    print("📱 Testing APK analysis endpoint...")
    
    # Create a dummy APK file for testing
    with tempfile.NamedTemporaryFile(suffix='.apk', delete=False) as tmp_file:
        tmp_file.write(b"PK\x03\x04")  # ZIP file signature (APK is a ZIP)
        tmp_file.write(b"dummy apk content for testing")
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'rb') as f:
            files = {'apk': ('test.apk', f, 'application/vnd.android.package-archive')}
            response = requests.post(f"{BASE_URL}/analyze-apk", files=files)
            
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        print("✅ APK analysis endpoint working")
        
    finally:
        os.unlink(tmp_file_path)

def test_permissions_summary():
    """Test permissions summarization"""
    print("🔐 Testing permissions summary endpoint...")
    
    test_permissions = [
        "android.permission.INTERNET",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.CAMERA",
        "android.permission.READ_CONTACTS"
    ]
    
    response = requests.post(
        f"{BASE_URL}/summarize-permissions",
        json={"permissions": test_permissions}
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    print("✅ Permissions summary working")

def test_emulator_endpoint():
    """Test emulator functionality"""
    print("📺 Testing emulator endpoint...")
    
    response = requests.get(f"{BASE_URL}/start-emulator")
    assert response.status_code == 200
    data = response.json()
    assert "emulator_started" in data
    print("✅ Emulator endpoint working")

def test_web_interface():
    """Test main web interface"""
    print("🌐 Testing web interface...")
    
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert "Forensic AI Hub" in response.text
    print("✅ Web interface loading correctly")

def test_log_feed():
    """Test log feed endpoint"""
    print("📋 Testing log feed endpoint...")
    
    response = requests.get(f"{BASE_URL}/log-feed")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "file_links" in data
    assert "api_calls" in data
    assert "transcripts" in data
    print("✅ Log feed endpoint working")

def run_all_tests():
    """Run all system tests"""
    print("🚀 Starting Forensic AI Tool System Tests")
    print("=" * 50)
    
    try:
        test_status_endpoints()
        test_voice_command()
        test_web_scraper()
        test_apk_analysis()
        test_permissions_summary()
        test_emulator_endpoint()
        test_web_interface()
        test_log_feed()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! System is working correctly.")
        print("=" * 50)
        
        # Print system summary
        print("\n📊 SYSTEM SUMMARY:")
        print("- ✅ Flask web server running")
        print("- ✅ All API endpoints functional")
        print("- ✅ Voice command processing working")
        print("- ✅ Web scraping functionality active")
        print("- ✅ APK analysis pipeline ready")
        print("- ✅ Permissions analysis working")
        print("- ✅ Emulator integration available")
        print("- ✅ Web interface fully functional")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)