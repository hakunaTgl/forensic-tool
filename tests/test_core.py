"""Test cases for core functionality."""

import pytest
import os
import sys
import tempfile

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from core.permissions_ai import (
    assess_permissions,
    get_risk_level,
    get_permission_details,
    DANGEROUS_PERMISSIONS
)
from core.status_check import check_status, check_component_status
from core.logs_export import get_logs_summary


class TestPermissionsAI:
    """Tests for permissions_ai module."""
    
    def test_assess_permissions_empty(self):
        """Test with empty permissions list."""
        assert assess_permissions([]) == 0
        assert assess_permissions(None) == 0
    
    def test_assess_permissions_single(self):
        """Test with single permission."""
        perms = ["android.permission.READ_SMS"]
        assert assess_permissions(perms) == 3
    
    def test_assess_permissions_multiple(self):
        """Test with multiple permissions."""
        perms = [
            "android.permission.READ_SMS",
            "android.permission.CAMERA"
        ]
        assert assess_permissions(perms) == 5
    
    def test_assess_permissions_unknown(self):
        """Test with unknown permission."""
        perms = ["android.permission.UNKNOWN_PERMISSION"]
        assert assess_permissions(perms) == 0
    
    def test_assess_permissions_string_input(self):
        """Test with comma-separated string input."""
        perms = "android.permission.READ_SMS, android.permission.CAMERA"
        assert assess_permissions(perms) == 5
    
    def test_get_risk_level(self):
        """Test risk level classification."""
        assert get_risk_level(0) == "None"
        assert get_risk_level(2) == "Low"
        assert get_risk_level(5) == "Medium"
        assert get_risk_level(8) == "High"
        assert get_risk_level(15) == "Critical"
    
    def test_get_permission_details(self):
        """Test permission details extraction."""
        perms = ["android.permission.READ_SMS"]
        details = get_permission_details(perms)
        
        assert len(details) == 1
        assert details[0]["permission"] == "android.permission.READ_SMS"
        assert details[0]["risk_score"] == 3
        assert details[0]["is_dangerous"] is True
    
    def test_get_permission_details_empty(self):
        """Test with empty permissions."""
        assert get_permission_details([]) == []
        assert get_permission_details(None) == []
    
    def test_dangerous_permissions_defined(self):
        """Test that dangerous permissions dictionary is populated."""
        assert len(DANGEROUS_PERMISSIONS) > 0
        assert "android.permission.READ_SMS" in DANGEROUS_PERMISSIONS


class TestStatusCheck:
    """Tests for status_check module."""
    
    def test_check_status(self):
        """Test basic status check."""
        status = check_status()
        
        assert status["status"] == "ok"
        assert "message" in status
        assert "components" in status
    
    def test_check_component_status_known(self):
        """Test checking known component."""
        status = check_component_status("core")
        
        assert status["status"] == "active"
    
    def test_check_component_status_unknown(self):
        """Test checking unknown component."""
        status = check_component_status("nonexistent")
        
        assert status["status"] == "unknown"


class TestLogsExport:
    """Tests for logs_export module."""
    
    def test_get_logs_summary(self):
        """Test logs summary generation."""
        summary = get_logs_summary()
        
        assert "total_scans" in summary
        assert "average_risk_score" in summary
        assert "high_risk_scans" in summary
        assert "timestamp" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
