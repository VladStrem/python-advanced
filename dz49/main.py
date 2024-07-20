from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from crud import (get_task, get_tasks,
                  create_task, update_task, delete_task)
from schemas.todo import Todo as TodoSchemas
from schemas.todo import TodoCreate, TodoUpdate
from models.todo import Todo, Base
from database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/todos/", response_model=TodoSchemas)
def todo_create(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_task(db=db, todo=todo)


@app.get("/todos/", response_model=list[TodoSchemas])
def todos_read(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_tasks(db=db, skip=skip, limit=limit)


@app.get("/todo/{todo_id}", response_model=TodoSchemas)
def todo_read(todo_id: int, db: Session = Depends(get_db)):
    db_todo = get_task(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return db_todo


@app.put("/todos/{todo_id}", response_model=TodoSchemas)
def todo_update(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = update_task(db=db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return db_todo


@app.delete("/todo/{todo_id}", response_model=TodoSchemas)
def todo_delete(todo_id: int, db: Session = Depends(get_db)):
    db_todo = delete_task(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return db_todo
