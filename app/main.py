from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models import Note as NoteModel
from app.schemas import Note, NoteCreate

app = FastAPI(title="Notes API")

@app.get("/")
def root():
    return {"message": "Welcome to Notes API! Go to /docs for Swagger"}

# 1. Создание заметки
@app.post("/notes/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    new_note = NoteModel(title=note.title, content=note.content)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

# 2. Получение всех заметок
@app.get("/notes/", response_model=List[Note])
async def read_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NoteModel))
    return result.scalars().all()

# 3. Получение ОДНОЙ заметки по ID
@app.get("/notes/{note_id}", response_model=Note)
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NoteModel).where(NoteModel.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

from app.schemas import Note, NoteCreate, NoteUpdate # Обнови импорт!

# 5. Обновление заметки методом PATCH
@app.patch("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, note_data: NoteUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NoteModel).where(NoteModel.id == note_id))
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = note_data.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(note, key, value)

    await db.commit()
    await db.refresh(note)
    return note

# 4. Удаление заметки
@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NoteModel).where(NoteModel.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await db.delete(note)
    await db.commit()
    return None