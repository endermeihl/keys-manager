#!/usr/bin/env python3
"""
CLI interface for Key Manager
"""

import argparse
import sys
import getpass
from keys_manager import KeyManager


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Secure Key Manager - Manage encrypted keys with password protection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a new key
  python cli.py generate --purpose "API Key"
  
  # List all key purposes
  python cli.py list
  
  # View a specific key
  python cli.py view --purpose "API Key"
  
  # Delete a key
  python cli.py delete --purpose "API Key"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a new secure key')
    generate_parser.add_argument('--purpose', required=True, help='Purpose/label for the key')
    generate_parser.add_argument('--storage', default='keys.enc', help='Storage file path (default: keys.enc)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all key purposes (no password required)')
    list_parser.add_argument('--storage', default='keys.enc', help='Storage file path (default: keys.enc)')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View a specific key')
    view_parser.add_argument('--purpose', required=True, help='Purpose/label of the key to view')
    view_parser.add_argument('--storage', default='keys.enc', help='Storage file path (default: keys.enc)')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a key')
    delete_parser.add_argument('--purpose', required=True, help='Purpose/label of the key to delete')
    delete_parser.add_argument('--storage', default='keys.enc', help='Storage file path (default: keys.enc)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize key manager
    km = KeyManager(storage_file=args.storage)
    
    try:
        if args.command == 'generate':
            # Prompt for password
            password = getpass.getpass('Enter password to encrypt the key: ')
            confirm_password = getpass.getpass('Confirm password: ')
            
            if password != confirm_password:
                print("Error: Passwords do not match", file=sys.stderr)
                sys.exit(1)
            
            if not password:
                print("Error: Password cannot be empty", file=sys.stderr)
                sys.exit(1)
            
            # Generate key
            generated_key = km.generate_key(args.purpose, password)
            print(f"✓ Key generated successfully!")
            print(f"Purpose: {args.purpose}")
            print(f"Key (24 characters): {generated_key}")
            print(f"\nIMPORTANT: Save this key securely. You'll need the password to view it again.")
        
        elif args.command == 'list':
            # List all purposes
            purposes = km.list_purposes()
            if not purposes:
                print("No keys stored yet.")
            else:
                print(f"Stored key purposes ({len(purposes)}):")
                for purpose in purposes:
                    print(f"  - {purpose}")
        
        elif args.command == 'view':
            # Prompt for password
            password = getpass.getpass('Enter password: ')
            
            # Retrieve key
            key = km.get_key(args.purpose, password)
            print(f"✓ Key retrieved successfully!")
            print(f"Purpose: {args.purpose}")
            print(f"Key: {key}")
        
        elif args.command == 'delete':
            # Prompt for password
            password = getpass.getpass('Enter password to delete the key: ')
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete the key '{args.purpose}'? Type 'yes' to confirm: ")
            if confirm.lower() != 'yes':
                print("Deletion cancelled.")
                sys.exit(0)
            
            # Delete key
            km.delete_key(args.purpose, password)
            print(f"✓ Key '{args.purpose}' deleted successfully!")
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
