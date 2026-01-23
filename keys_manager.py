#!/usr/bin/env python3
"""
Key Manager - A secure key management tool
Manages encrypted keys with password protection
"""

import json
import os
import secrets
import string
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class KeyManager:
    """Manages secure storage and retrieval of encrypted keys"""

    def __init__(self, storage_file='keys.enc'):
        """Initialize the key manager with a storage file"""
        self.storage_file = Path(storage_file)
        self.key_length = 48  # Length of random part (excluding prefix)
        self.default_prefix = 'sk-'
        
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())
    
    def _get_cipher(self, password: str, salt: bytes):
        """Get Fernet cipher from password"""
        # Derive a 32-byte key using PBKDF2
        key = self._derive_key(password, salt)
        # Fernet requires base64-encoded 32-byte key
        fernet_key = base64.urlsafe_b64encode(key)
        return Fernet(fernet_key)
    
    def _load_data(self):
        """Load encrypted data from storage file"""
        if not self.storage_file.exists():
            return {'salt': None, 'keys': {}}
        
        with open(self.storage_file, 'r') as f:
            data = json.load(f)
            # Convert salt from hex string back to bytes
            if data.get('salt'):
                data['salt'] = bytes.fromhex(data['salt'])
            return data
    
    def _save_data(self, data):
        """Save encrypted data to storage file"""
        # Convert salt to hex string for JSON serialization
        save_data = data.copy()
        if save_data.get('salt'):
            save_data['salt'] = save_data['salt'].hex()
        
        with open(self.storage_file, 'w') as f:
            json.dump(save_data, f, indent=2)
    
    def generate_key(self, purpose: str, password: str, prefix: str = None) -> str:
        """Generate a secure API-style key (e.g., sk-xxx...) and store it encrypted"""
        # Use default prefix if not specified
        if prefix is None:
            prefix = self.default_prefix

        # Generate secure random key using alphanumeric characters only (API-style)
        alphabet = string.ascii_letters + string.digits
        random_part = ''.join(secrets.choice(alphabet) for _ in range(self.key_length))
        secure_key = f"{prefix}{random_part}"
        
        # Load existing data
        data = self._load_data()
        
        # Generate or reuse salt
        if data['salt'] is None:
            data['salt'] = os.urandom(16)
        
        salt = data['salt']
        
        # Check if purpose already exists
        if purpose in data['keys']:
            raise ValueError(f"Key with purpose '{purpose}' already exists")
        
        # Encrypt the key
        cipher = self._get_cipher(password, salt)
        encrypted_key = cipher.encrypt(secure_key.encode())
        
        # Store encrypted key (as base64 string for JSON compatibility)
        data['keys'][purpose] = base64.b64encode(encrypted_key).decode('utf-8')
        
        # Save data
        self._save_data(data)
        
        return secure_key
    
    def list_purposes(self) -> list:
        """List all key purposes without requiring password"""
        data = self._load_data()
        return list(data['keys'].keys())
    
    def get_key(self, purpose: str, password: str) -> str:
        """Retrieve a key by purpose using password"""
        data = self._load_data()
        
        if purpose not in data['keys']:
            raise ValueError(f"No key found with purpose '{purpose}'")
        
        if data['salt'] is None:
            raise ValueError("No keys stored yet")
        
        # Decrypt the key
        encrypted_key = base64.b64decode(data['keys'][purpose])
        
        cipher = self._get_cipher(password, data['salt'])
        try:
            decrypted_key = cipher.decrypt(encrypted_key)
            return decrypted_key.decode('utf-8')
        except Exception as e:
            # Fernet raises InvalidToken for decryption failures
            # This typically means wrong password or corrupted data
            raise ValueError("Invalid password")
    
    def delete_key(self, purpose: str, password: str):
        """Delete a key by purpose using password"""
        # First verify password by trying to decrypt
        _ = self.get_key(purpose, password)
        
        # If password is correct, delete the key
        data = self._load_data()
        del data['keys'][purpose]
        
        # If no keys left, clear salt as well
        if not data['keys']:
            data['salt'] = None
        
        self._save_data(data)
