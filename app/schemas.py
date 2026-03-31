from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Общие поля которые есть при создании и при чтении
class NoteBase(BaseModel):
    title: str
    content: str

# Эту схему мы используем, когда КЛИЕНТ присылает нам данные (POST-запрос)
class NoteCreate(NoteBase):
    pass

# Эту схему мы используем, когда ОТПРАВЛЯЕМ данные клиенту (Response)
class Note(NoteBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Схема для обновления заметки
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None