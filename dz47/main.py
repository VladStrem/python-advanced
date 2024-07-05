from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from models import TodoModel, Base
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todo", response_class=HTMLResponse)
def todo_main(request: Request, db: Session = Depends(get_db)):
    stmt = select(TodoModel)
    todos = db.scalars(stmt).all()
    return templates.TemplateResponse("todo.html", {"request": request, "todo_list": todos})


@app.post("/todo/add")
def todo_add(title: str = Form(), db: Session = Depends(get_db)):
    new_todo = TodoModel(title=title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return RedirectResponse(url=app.url_path_for("todo_main"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/todo/update/{id}")
def todo_update(id: int, db: Session = Depends(get_db)):
    stmt = select(TodoModel).where(TodoModel.id == id)
    result = db.execute(stmt)
    todo = result.scalars().first()
    if todo:
        todo.complete = not todo.complete
        db.commit()
    return RedirectResponse(url=app.url_path_for("todo_main"), status_code=status.HTTP_302_FOUND)


@app.get("/todo/delete/{id}")
def todo_delete(id: int, db: Session = Depends(get_db)):
    stmt = select(TodoModel).where(TodoModel.id == id)
    result = db.execute(stmt)
    todo = result.scalars().first()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url=app.url_path_for("todo_main"), status_code=status.HTTP_302_FOUND)
