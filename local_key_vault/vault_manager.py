from cryptography.fernet import Fernet


class LocalSecretsScope:
    def __init__(self, scope_path, key):
        self.scope_path = scope_path
        self.fernet = Fernet(key)

    def set_secret(self, key, value):
        encrypted_value = self.fernet.encrypt(value.encode())
        with open(self.scope_path / key, 'wb') as f:
            f.write(encrypted_value)

    def get_secret(self, key):
        try:
            with open(self.scope_path / key, 'rb') as f:
                encrypted_value = f.read()
            decrypted_value = self.fernet.decrypt(encrypted_value)
            return decrypted_value.decode()
        except FileNotFoundError:
            raise KeyError(f"Secret '{key}' not found in scope")

    def list_secrets(self):
        return [f.name for f in self.scope_path.iterdir() if f.is_file() and f.name != '.salt']

    def delete_secret(self, key):
        secret_path = self.scope_path / key
        if secret_path.exists():
            secret_path.unlink()
        else:
            raise KeyError(f"Secret '{key}' not found in scope")