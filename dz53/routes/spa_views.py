from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.templating import Jinja2Templates
from services import crud_user


templates = Jinja2Templates(directory="templates")

router = APIRouter()

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if user and user.is_superuser and credentials.password == "itstep":
        return user
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Basic"},
    )


@router.get("/spa", response_class=HTMLResponse)
def get_spa(request: Request, credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    # authenticate(credentials, db)
    # users = crud_user.get_users(db=db)
    # return templates.TemplateResponse(request=request, name="spa.html", context={"users": users})
    authenticate(credentials, db)
    with open("templates/spa.html") as f:
        return HTMLResponse(content=f.read())


# @router.delete("/users/{user_id}", response_model=dict)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#
#     db.delete(user)
#     db.commit()
#
#     return {"message": "User deleted successfully"}
