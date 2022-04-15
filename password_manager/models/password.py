from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class PasswordModel(BaseModel):
    key: str = Field(default_factory=lambda: str(uuid4()))
    name: str = ''
    password: str = ''
    url: str = ''
    note: str = ''
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_edited_at: datetime = Field(default_factory=datetime.utcnow)

    def search_attributes(self):
        attribute_names = ['name', 'url', 'note']

        return [getattr(self, attribute_name) for attribute_name in attribute_names]
