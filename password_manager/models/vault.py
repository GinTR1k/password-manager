from datetime import datetime

from pydantic import BaseModel

from password_manager.models.password import PasswordModel


class VaultModel(BaseModel):
    passwords: dict[str, PasswordModel]
    last_update_at: datetime
