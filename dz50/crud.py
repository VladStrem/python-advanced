from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.todo import TodoCreate, TodoUpdate
from models.todo import Todo


def get_task(db: Session, todo_id: int):
    stmt = select(Todo).filter(Todo.id == todo_id)
    result = db.execute(statement=stmt).scalar_one_or_none()
    return result


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(Todo).offset(skip).limit(limit)
    result = db.scalars(stmt).all()
    return result


def create_task(db: Session, todo: TodoCreate):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_task(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = get_task(db, todo_id)
    if db_todo is None:
        return None
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_task(db: Session, todo_id: int):
    db_todo = get_task(db, todo_id)
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo        
