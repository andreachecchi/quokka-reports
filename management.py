#!/usr/bin/env python3
"""
Management script for user management.
Interactive menu interface to manage users.json
"""

import json
import hashlib
import re
import sys
import getpass
from datetime import datetime
from pathlib import Path


USERS_FILE = Path(__file__).parent / "users.json"


class UserManager:
    """Manager for loading, modifying, and saving users."""

    def __init__(self, filepath: Path = USERS_FILE):
        self.filepath = filepath
        self.users = []
        self.load()

    def load(self):
        """Load users from JSON file."""
        if not self.filepath.exists():
            self.users = []
            return

        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.users = data.get('users', [])

    def save(self):
        """Save users to JSON file."""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump({'users': self.users}, f, indent=2, ensure_ascii=False)

    def get_user_by_id(self, user_id: int):
        """Find user by ID."""
        for user in self.users:
            if user.get('id') == user_id:
                return user
        return None

    def get_user_by_username(self, username: str, exclude_id: int = None):
        """Find user by username (optionally excluding an ID)."""
        for user in self.users:
            if user.get('username') == username:
                if exclude_id is not None and user.get('id') == exclude_id:
                    continue
                return user
        return None

    def hash_password(self, password: str) -> str:
        """Calculate SHA256 hash of a password."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def list_users(self):
        """List all users."""
        if not self.users:
            print("\nNo users found.")
            return

        print("\n" + "=" * 100)
        print(f"{'ID':<6} {'Name':<20} {'Username':<15} {'Email':<25} {'Status':<10}")
        print("=" * 100)

        for user in self.users:
            user_id = user.get('id', '')
            name = user.get('name', '')[:18]
            username = user.get('username', '')[:13]
            email = user.get('email', '')[:23]
            is_active = user.get('active', user.get('isactive', True))
            status = "Active" if is_active else "Inactive"

            print(f"{user_id:<6} {name:<20} {username:<15} {email:<25} {status:<10}")

        print("=" * 100)
        print(f"Total users: {len(self.users)}")


def print_user_details(user):
    """Print user details."""
    print("\n" + "-" * 40)
    print(f"ID:          {user.get('id')}")
    print(f"Name:        {user.get('name')}")
    print(f"Username:    {user.get('username')}")
    print(f"Email:       {user.get('email')}")
    print(f"Group:       {user.get('group', 'N/A')}")
    print(f"Locale:      {user.get('locale', 'N/A')}")
    print(f"Created:     {user.get('created', 'N/A')}")
    print(f"Updated:     {user.get('updated', 'N/A')}")
    is_active = user.get('active', user.get('isactive', True))
    print(f"Status:      {'Active' if is_active else 'Inactive'}")
    print("-" * 40)


def read_input(prompt: str, required: bool = True, default: str = None) -> str:
    """Read user input."""
    if default is not None:
        prompt = f"{prompt} [default: {default}]"
    value = input(prompt + ": ").strip()
    if not value and default is not None:
        return default
    if not value and required:
        print("Error: value is required.")
        return read_input(prompt, required, default)
    return value


def read_yes_no(prompt: str, default: bool = True) -> bool:
    """Read yes/no input."""
    default_str = "Yes" if default else "No"
    value = input(f"{prompt} [Y/n] (default: {default_str}): ").strip().lower()
    if not value:
        return default
    return value in ('y', 'yes', '1')


def read_password(prompt: str) -> str:
    """Read password input (masked with asterisks)."""
    return getpass.getpass(prompt + ": ")


def menu_principal():
    """Main menu."""
    print("\n" + "=" * 40)
    print("   USER MANAGEMENT - MAIN MENU")
    print("=" * 40)
    print("1. List all users")
    print("2. Show user details")
    print("3. Change user password")
    print("4. Update user data")
    print("5. Deactivate user")
    print("6. Create new user")
    print("7. Delete user")
    print("8. Save changes")
    print("0. Exit")
    print("=" * 40)


def opzione_list_users(manager: UserManager):
    """Option 1: List all users."""
    manager.list_users()


def opzione_show_user(manager: UserManager):
    """Option 2: Show user details."""
    try:
        user_id = int(read_input("Enter user ID"))
        user = manager.get_user_by_id(user_id)
        if user:
            print_user_details(user)
        else:
            print(f"\nError: user with ID {user_id} not found.")
    except ValueError:
        print("\nError: please enter a valid number.")


def opzione_change_password(manager: UserManager):
    """Option 3: Change user password."""
    try:
        user_id = int(read_input("Enter user ID"))
        user = manager.get_user_by_id(user_id)
        if not user:
            print(f"\nError: user with ID {user_id} not found.")
            return

        print(f"Changing password for: {user.get('name')} ({user.get('username')})")
        new_password = read_password("New password")
        confirm_password = read_password("Confirm new password")

        if new_password != confirm_password:
            print("\nError: passwords do not match.")
            return

        user['password'] = manager.hash_password(new_password)
        user['updated'] = datetime.utcnow().isoformat()
        print("\nPassword updated successfully!")
        print_user_details(user)

    except ValueError:
        print("\nError: please enter a valid number.")


def opzione_update_user(manager: UserManager):
    """Option 4: Update user data."""
    try:
        user_id = int(read_input("Enter user ID to modify"))
        user = manager.get_user_by_id(user_id)
        if not user:
            print(f"\nError: user with ID {user_id} not found.")
            return

        print(f"\nModifying user: {user.get('name')} ({user.get('username')})")
        print("Press ENTER to keep the current value.")

        # Collect new values
        new_name = read_input("Name", required=False, default=user.get('name', ''))
        new_username = read_input("Username", required=False, default=user.get('username', ''))
        new_email = read_input("Email", required=False, default=user.get('email', ''))
        new_group = read_input("Group", required=False, default=user.get('group', ''))
        new_locale = read_input("Locale", required=False, default=user.get('locale', ''))
        new_isactive = read_yes_no("Active?", default=user.get('active', user.get('isactive', True)))

        # Validations
        errors = []

        # Username unique
        if new_username and new_username != user.get('username'):
            existing = manager.get_user_by_username(new_username, exclude_id=user_id)
            if existing:
                errors.append(f"Username '{new_username}' already in use.")

        # Email valid
        if new_email and not manager.validate_email(new_email):
            errors.append(f"Email '{new_email}' is not valid.")

        # Confirmation and application
        if errors:
            print("\nError: the following validations failed:")
            for err in errors:
                print(f"  - {err}")
            return

        # Apply changes
        if new_name:
            user['name'] = new_name
        if new_username:
            user['username'] = new_username
        if new_email:
            user['email'] = new_email
        if new_group:
            user['group'] = new_group
        if new_locale:
            user['locale'] = new_locale

        user['active'] = new_isactive
        user['updated'] = datetime.utcnow().isoformat()

        print("\nData updated successfully!")
        print_user_details(user)

    except ValueError:
        print("\nError: please enter a valid number.")


def opzione_deactivate_user(manager: UserManager):
    """Option 5: Deactivate user."""
    try:
        user_id = int(read_input("Enter user ID to deactivate"))
        user = manager.get_user_by_id(user_id)
        if not user:
            print(f"\nError: user with ID {user_id} not found.")
            return

        print(f"\nDeactivating user: {user.get('name')} ({user.get('username')})")
        if read_yes_no("Are you sure you want to deactivate this user?", default=False):
            user['active'] = False
            user['updated'] = datetime.utcnow().isoformat()
            print("\nUser deactivated!")
            print_user_details(user)
        else:
            print("\nOperation cancelled.")

    except ValueError:
        print("\nError: please enter a valid number.")


def opzione_save(manager: UserManager):
    """Option 8: Save changes."""
    if not manager.users:
        print("\nNo users to save.")
        return

    print("\nData in memory:")
    manager.list_users()

    if read_yes_no("\nSave changes to file?", default=True):
        manager.save()
        print("\nChanges saved successfully!")
    else:
        print("\nSave cancelled.")


def opzione_create_user(manager: UserManager):
    """Option 6: Create new user."""
    print("\n--- CREATE NEW USER ---")
    
    # Collect user data
    name = read_input("Name", required=True)
    username = read_input("Username", required=True)
    email = read_input("Email", required=True)
    
    # Password input (masked) with confirmation
    password = read_password("Password")
    confirm_password = read_password("Confirm password")
    
    if password != confirm_password:
        print("\nError: passwords do not match.")
        return
    
    group = read_input("Group", required=False, default="users")
    locale = read_input("Locale", required=False, default="en")
    is_active = read_yes_no("Active?", default=True)
    
    # Validations
    errors = []
    
    # Check username uniqueness
    if manager.get_user_by_username(username):
        errors.append(f"Username '{username}' already in use.")
    
    # Validate email
    if not manager.validate_email(email):
        errors.append(f"Email '{email}' is not valid.")
    
    if errors:
        print("\nError: the following validations failed:")
        for err in errors:
            print(f"  - {err}")
        return
    
    # Create new user
    new_id = max((u.get('id', 0) for u in manager.users), default=0) + 1
    
    new_user = {
        'id': new_id,
        'name': name,
        'username': username,
        'email': email,
        'password': manager.hash_password(password),
        'group': group,
        'locale': locale,
        'active': is_active,
        'created': datetime.utcnow().isoformat(),
        'updated': datetime.utcnow().isoformat()
    }
    
    manager.users.append(new_user)
    print("\nUser created successfully!")
    print_user_details(new_user)


def opzione_delete_user(manager: UserManager):
    """Option 7: Delete user."""
    try:
        user_id = int(read_input("Enter user ID to delete"))
        user = manager.get_user_by_id(user_id)
        
        if not user:
            print(f"\nError: user with ID {user_id} not found.")
            return
        
        print(f"\nDeleting user: {user.get('name')} ({user.get('username')})")
        
        if read_yes_no("Are you sure you want to delete this user?", default=False):
            manager.users = [u for u in manager.users if u.get('id') != user_id]
            print("\nUser deleted!")
        else:
            print("\nOperation cancelled.")
            
    except ValueError:
        print("\nError: please enter a valid number.")


def main():
    """Main function."""
    manager = UserManager()

    print("\n" + "=" * 50)
    print("  Application Management - User System")
    print("=" * 50)
    print(f"Users file: {USERS_FILE}")
    print(f"Users loaded: {len(manager.users)}")

    while True:
        menu_principal()
        scelta = input("Select an option (0-6): ").strip()

        if scelta == '1':
            opzione_list_users(manager)
        elif scelta == '2':
            opzione_show_user(manager)
        elif scelta == '3':
            opzione_change_password(manager)
        elif scelta == '4':
            opzione_update_user(manager)
        elif scelta == '5':
            opzione_deactivate_user(manager)
        elif scelta == '6':
            opzione_create_user(manager)
        elif scelta == '7':
            opzione_delete_user(manager)
        elif scelta == '8':
            opzione_save(manager)
        elif scelta == '0':
            print("\nExiting the program.")
            sys.exit(0)
        else:
            print("\nInvalid option. Please try again.")


if __name__ == '__main__':
    main()
