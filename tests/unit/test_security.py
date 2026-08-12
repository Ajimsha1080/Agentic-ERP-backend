import pytest
import os
from packages.security.utils import (
    sanitize_input,
    check_admin_privileges,
    check_system_maintenance,
    detect_suspicious_activity,
    validate_tenant_access
)
from packages.security.password import enforce_password_expiration

def test_sanitize_input():
    dirty = "<script>alert('xss')</script>"
    clean = sanitize_input(dirty)
    assert "&lt;script&gt;" in clean
    assert "<script>" not in clean

def test_check_admin_privileges():
    admin_user = {"is_admin": True}
    superuser = {"is_superuser": True}
    standard_user = {"is_admin": False, "is_superuser": False}
    
    assert check_admin_privileges(admin_user) is True
    assert check_admin_privileges(superuser) is True
    assert check_admin_privileges(standard_user) is False

def test_check_system_maintenance(monkeypatch):
    monkeypatch.setenv("MAINTENANCE_MODE", "true")
    assert check_system_maintenance() is True
    
    monkeypatch.setenv("MAINTENANCE_MODE", "false")
    assert check_system_maintenance() is False

def test_enforce_password_expiration(monkeypatch):
    monkeypatch.setenv("ENFORCE_PW_EXPIRATION", "false")
    assert enforce_password_expiration() is False

def test_detect_suspicious_activity():
    # Basic implementation returns False for now
    assert detect_suspicious_activity("user123", "login") is False

def test_validate_tenant_access():
    # Basic implementation returns True
    assert validate_tenant_access("user123", "tenant456") is True
