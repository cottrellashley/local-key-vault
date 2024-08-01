import os
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from .vault_manager import LocalSecretsScope


def get_application_directory():
    home = Path.home()
    app_dir = home / 'local_key_vault'
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


class LocalKeyVault:
    def __init__(self, base_path=None):
        if base_path is None:
            base_path = get_application_directory()
        self.base_path = Path(base_path)

    def create_scope(self, scope_name, password):
        scope_path = self.base_path / scope_name
        if scope_path.exists():
            raise ValueError(f"Scope '{scope_name}' already exists")

        scope_path.mkdir(parents=True, exist_ok=True)

        # Generate a key from the password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        # Store the salt
        with open(scope_path / '.salt', 'wb') as f:
            f.write(salt)

        return LocalSecretsScope(scope_path, key)

    def get_scope(self, scope_name, password):
        scope_path = self.base_path / scope_name
        if not scope_path.exists():
            raise ValueError(f"Scope '{scope_name}' does not exist")

        with open(scope_path / '.salt', 'rb') as f:
            salt = f.read()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

        return LocalSecretsScope(scope_path, key)
