"""
Authentication Module

Provides user authentication functionality using SHA256 hashed passwords
stored in the users.json file.

This module handles:
- Loading users from users.json
- Hashing passwords with SHA256
- Validating user credentials
- Checking user activity status
"""

import json
import hashlib
from pathlib import Path
from config import USERS_FILE


def hash_password(password: str) -> str:
    """
    Hash a password using SHA256.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        SHA256 hash of the password as a hexadecimal string
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def load_users() -> list:
    """
    Load all users from the users.json file.
    
    Returns:
        List of user dictionaries
    """
    if not USERS_FILE.exists():
        return []
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('users', [])
    except (json.JSONDecodeError, IOError):
        return []


def get_user_by_username(username: str) -> dict | None:
    """
    Find a user by username.
    
    Args:
        username: Username to search for
        
    Returns:
        User dictionary if found, None otherwise
    """
    users = load_users()
    
    for user in users:
        if user.get('username') == username:
            return user
    
    return None


def authenticate_user(username: str, password: str) -> dict | None:
    """
    Authenticate a user with username and password.
    
    The password is hashed with SHA256 and compared to the stored hash.
    
    Args:
        username: Username provided by the user
        password: Plain text password provided by the user
        
    Returns:
        User dictionary if authentication succeeds, None otherwise
    """
    user = get_user_by_username(username)
    
    if user is None:
        return None
    
    # Check if user is active (supports both 1 and true values)
    if not is_user_active(user):
        return None
    
    # Hash the provided password and compare with stored hash
    provided_hash = hash_password(password)
    stored_hash = user.get('password', '')
    
    if provided_hash == stored_hash:
        return user
    
    return None


def is_user_active(user: dict) -> bool:
    """
    Check if a user account is active.
    
    Args:
        user: User dictionary
        
    Returns:
        True if the user is active, False otherwise
    """
    isactive = user.get('isactive')
    return isactive is True or isactive == 1


def get_user_group(user: dict) -> str:
    """
    Get the group of a user.
    
    Args:
        user: User dictionary
        
    Returns:
        User group name
    """
    return user.get('group', 'default')
