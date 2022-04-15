import json
import os
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2

from password_manager import config
from password_manager.exceptions import MasterPasswordError, VaultDoesNotExist, WrongVaultFormat
from password_manager.models.password import PasswordModel
from password_manager.models.vault import VaultModel


class Vault:
    def __init__(self):
        self.__vault: VaultModel | None = None
        self.__master_password: bytes | None = None

    @property
    def passwords(self) -> list[PasswordModel]:
        return list(self.__vault.passwords.values()) if self.__vault else []

    def unlock(self, master_password: str):
        if not self.does_vault_file_exists():
            raise VaultDoesNotExist()

        self.__master_password = PBKDF2(master_password.encode().hex(), b'', 32, count=1_000_000, hmac_hash_module=SHA512)
        self.__vault = self._open_vault_file()

    def create(self, master_password: str):
        self.__master_password = PBKDF2(master_password.encode().hex(), b'', 32, count=1_000_000, hmac_hash_module=SHA512)
        self.__vault = VaultModel(passwords={}, last_update_at=datetime.utcnow())
        self._update_vault_file(self.__vault)

    def find_passwords(self, name: str) -> list[PasswordModel]:
        result = []
        search_name = name.lower()

        for password in self.__vault.passwords.values():
            for attribute in password.search_attributes():
                if search_name.lower() in attribute.lower():
                    result.append(password)
                    break

        return result

    def add_password(self, password: PasswordModel):
        self.__vault.passwords[password.key] = password
        self.__vault.last_update_at = datetime.utcnow()
        self._update_vault_file(self.__vault)

    def delete_password(self, key: str):
        del self.__vault.passwords[key]
        self.__vault.last_update_at = datetime.utcnow()
        self._update_vault_file(self.__vault)

    def update_password(self, password: PasswordModel):
        last_edited_at = datetime.utcnow()
        password.created_at = self.__vault.passwords[password.key].created_at
        password.last_edited_at = last_edited_at

        self.__vault.passwords[password.key] = password
        self.__vault.last_update_at = last_edited_at
        self._update_vault_file(self.__vault)

    @staticmethod
    def does_vault_file_exists() -> bool:
        return os.path.exists(config.VAULT_FILE_PATH)

    def _open_vault_file(self) -> VaultModel:
        with open(config.VAULT_FILE_PATH, 'rb') as f:
            file_content = f.read()

        cipher = AES.new(self.__master_password, AES.MODE_EAX, config.IV)
        decrypted_file_content = cipher.decrypt(file_content)

        try:
            json_data = json.loads(decrypted_file_content)
        except UnicodeDecodeError as e:
            raise MasterPasswordError() from e

        return VaultModel(**json_data)

    def _update_vault_file(self, vault_data: VaultModel):
        cipher = AES.new(self.__master_password, AES.MODE_EAX, config.IV)
        encrypted_data = cipher.encrypt(vault_data.json().encode())

        with open(config.VAULT_FILE_PATH, 'wb') as f:
            f.write(encrypted_data)
