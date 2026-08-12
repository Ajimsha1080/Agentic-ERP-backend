"""
Password utilities.

Handles password validation, strength checking, and security policies.
"""

import re
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordPolicy:
    """Password policy definition."""

    def __init__(
        self,
        min_length: int = 8,
        max_length: int = 64,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_numbers: bool = True,
        require_special: bool = True,
        require_non_ascii: bool = False,
        prevent_reuse: bool = True,
        prevent_common: bool = True,
        prevent_sequences: bool = True
    ):
        """Initialize password policy.

        Args:
            min_length: Minimum password length
            max_length: Maximum password length
            require_uppercase: Require uppercase letters
            require_lowercase: Require lowercase letters
            require_numbers: Require numbers
            require_special: Require special characters
            require_non_ascii: Require non-ASCII characters
            prevent_reuse: Prevent password reuse
            prevent_common: Prevent common passwords
            prevent_sequences: Prevent sequential characters
        """
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_numbers = require_numbers
        self.require_special = require_special
        self.require_non_ascii = require_non_ascii
        self.prevent_reuse = prevent_reuse
        self.prevent_common = prevent_common
        self.prevent_sequences = prevent_sequences

    def validate(self, password: str, previous_passwords: List[str] = None) -> List[str]:
        """Validate password against policy.

        Args:
            password: Password to validate
            previous_passwords: List of previous passwords for reuse check

        Returns:
            List[str]: List of validation errors, empty if valid
        """
        errors = []

        # Length check
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        elif len(password) > self.max_length:
            errors.append(f"Password must be at most {self.max_length} characters long")

        # Character type checks
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if self.require_numbers and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if self.require_special and not re.search(r'[^a-zA-Z0-9]', password):
            errors.append("Password must contain at least one special character")
        
        if self.require_non_ascii and not re.search(r'[^\x00-\x7F]', password):
            errors.append("Password must contain at least one non-ASCII character")

        # Prevent common passwords
        common_passwords = [
            "password", "123456", "12345678", "123456789", "1234567890",
            "qwerty", "abc123", "letmein", "welcome", "admin",
            "password1", "123123", "password123", "111111", "123321",
            "1234567", "1234qwer", "admin123", "welcome1", "monkey"
        ]
        
        if self.prevent_common and password.lower() in common_passwords:
            errors.append("Password is too common and not allowed")

        # Prevent sequential characters
        if self.prevent_sequences:
            sequences = [
                "0123456789", "9876543210",
                "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba",
                "qwertyuiop", "asdfghjkl", "zxcvbnm"
            ]
            
            for sequence in sequences:
                if sequence in password.lower():
                    errors.append("Password contains sequential characters")
                    break
        
        # Prevent password reuse
        if self.prevent_reuse and previous_passwords and password in previous_passwords:
            errors.append("Password has been used before and cannot be reused")

        return errors


def hash_password(password: str) -> str:
    """Hash password.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        bool: True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password: str) -> str:
    """Generate password hash.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return hash_password(password)


# Default password policy
default_password_policy = PasswordPolicy()


def validate_password_strength(password: str) -> tuple[bool, List[str]]:
    """Validate password strength.

    Args:
        password: Password to validate

    Returns:
        tuple: (is_valid, errors)
    """
    errors = default_password_policy.validate(password)
    return len(errors) == 0, errors


def is_password_strong_enough(password: str) -> bool:
    """Check if password is strong enough.

    Args:
        password: Password to check

    Returns:
        bool: True if password is strong enough
    """
    is_valid, _ = validate_password_strength(password)
    return is_valid


def get_password_strength_feedback(password: str) -> str:
    """Get password strength feedback.

    Args:
        password: Password to check

    Returns:
        str: Feedback message
    """
    is_valid, errors = validate_password_strength(password)
    
    if is_valid:
        return "Password is strong enough"
    else:
        return "Password is too weak: " + ", ".join(errors)


def suggest_strong_password() -> str:
    """Suggest a strong password.

    Returns:
        str: Strong password suggestion
    """
    import random
    import string

    # Generate random components
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice('!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    # Fill with random characters
    length = 12
    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    random_chars = ''.join(random.choice(all_chars) for _ in range(remaining_length))
    
    # Combine and shuffle
    password = uppercase + lowercase + digit + special + random_chars
    password_list = list(password)
    random.shuffle(password_list)
    
    return ''.join(password_list)


def enforce_password_change_after_first_login() -> bool:
    """Enforce password change after first login.

    Returns:
        bool: True to enforce password change
    """
    import os
    return os.environ.get("ENFORCE_FIRST_LOGIN_PW_CHANGE", "true").lower() == "true"


def enforce_password_expiration() -> bool:
    """Enforce password expiration.

    Returns:
        bool: True to enforce password expiration
    """
    import os
    return os.environ.get("ENFORCE_PW_EXPIRATION", "true").lower() == "true"


def get_password_expiration_period() -> int:
    """Get password expiration period in days.

    Returns:
        int: Password expiration period in days
    """
    import os
    try:
        return int(os.environ.get("PW_EXPIRATION_DAYS", "90"))
    except ValueError:
        return 90
