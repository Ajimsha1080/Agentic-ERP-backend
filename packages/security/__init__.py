"""
Security package.

Provides comprehensive security functionality for the application.
"""

from .auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    verify_password_reset_token,
    get_current_user,
    get_current_active_user,
    require_permissions,
    get_current_admin_user
)

from .middleware import (
    SecurityMiddleware,
    get_security_middleware,
    verify_token_middleware,
    require_tenant_middleware,
    APIKeyAuth,
    get_api_key_auth,
    security_middleware_stack
)

from .password import (
    PasswordPolicy,
    hash_password,
    verify_password as verify_password_hash,
    generate_password_hash,
    validate_password_strength,
    is_password_strong_enough,
    get_password_strength_feedback,
    suggest_strong_password,
    enforce_password_change_after_first_login,
    enforce_password_expiration,
    get_password_expiration_period
)

from .rates import (
    RateLimiter,
    get_rate_limiter,
    SecurityRateLimits,
    check_endpoint_rate_limit,
    get_rate_limit_headers,
    cleanup_rate_limit_data
)

from .utils import (
    generate_secure_token,
    generate_uuid,
    generate_api_key,
    generate_verification_code,
    validate_email_address,
    sanitize_input,
    validate_phone_number,
    validate_url,
    hash_sensitive_data,
    mask_sensitive_data,
    validate_file_type,
    sanitize_filename,
    generate_secure_filename,
    check_admin_privileges,
    check_system_maintenance,
    get_client_info,
    log_security_event,
    detect_suspicious_activity,
    validate_tenant_access,
    validate_organization_access,
    generate_secure_session_id,
    validate_session,
    expire_session,
    get_security_headers,
    check_cors_origin
)

__all__ = [
    # Auth functions
    'create_access_token',
    'create_refresh_token',
    'verify_password',
    'get_password_hash',
    'get_current_user',
    'require_permissions',
    'create_password_reset_token',
    'verify_password_reset_token',
    # Security classes
    'SecurityMiddleware',
]
