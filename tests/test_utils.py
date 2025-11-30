"""Test cases for utility modules."""

import pytest
import os
import sys
import tempfile

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from utils.ai_helper import (
    summarize_permissions,
    get_ai_recommendation,
    get_permission_description
)
from utils.status_check import get_system_status, check_dependencies


class TestAIHelper:
    """Tests for ai_helper module."""
    
    def test_summarize_permissions_empty(self):
        """Test with empty permissions."""
        assert summarize_permissions([]) == "No permissions found."
        assert summarize_permissions(None) == "No permissions found."
    
    def test_summarize_permissions_single(self):
        """Test with single permission."""
        perms = ["android.permission.INTERNET"]
        summary = summarize_permissions(perms)
        
        assert "1 permissions" in summary
    
    def test_summarize_permissions_dangerous(self):
        """Test with dangerous permissions."""
        perms = ["android.permission.READ_SMS", "android.permission.CAMERA"]
        summary = summarize_permissions(perms)
        
        assert "dangerous" in summary.lower()
    
    def test_summarize_permissions_string_input(self):
        """Test with comma-separated string input."""
        perms = "android.permission.INTERNET, android.permission.CAMERA"
        summary = summarize_permissions(perms)
        
        assert "2 permissions" in summary
    
    def test_get_ai_recommendation_empty(self):
        """Test recommendation with empty permissions."""
        result = get_ai_recommendation([], 0)
        
        assert result["risk_level"] == "none"
        assert len(result["concerns"]) == 0
    
    def test_get_ai_recommendation_high_risk(self):
        """Test recommendation with high risk score."""
        perms = ["android.permission.READ_SMS"]
        result = get_ai_recommendation(perms, 10)
        
        assert result["risk_level"] == "critical"
        assert len(result["recommendations"]) > 0
    
    def test_get_ai_recommendation_low_risk(self):
        """Test recommendation with low risk score."""
        perms = ["android.permission.INTERNET"]
        result = get_ai_recommendation(perms, 1)
        
        assert result["risk_level"] == "low"
    
    def test_get_permission_description_known(self):
        """Test description for known permission."""
        desc = get_permission_description("android.permission.INTERNET")
        
        assert "network" in desc.lower()
    
    def test_get_permission_description_unknown(self):
        """Test description for unknown permission."""
        desc = get_permission_description("android.permission.UNKNOWN_PERM")
        
        assert "UNKNOWN_PERM" in desc


class TestStatusCheckUtils:
    """Tests for status_check utility module."""
    
    def test_get_system_status(self):
        """Test system status retrieval."""
        status = get_system_status()
        
        assert status["status"] == "ok"
        assert "details" in status
        assert "components" in status
    
    def test_check_dependencies(self):
        """Test dependency check."""
        deps = check_dependencies()
        
        assert "dependencies" in deps
        assert "all_available" in deps
        # Check that it returns boolean values
        for key, value in deps["dependencies"].items():
            assert isinstance(value, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
