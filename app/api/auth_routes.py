from fastapi import APIRouter, Depends , HTTPException,status
from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal
from app.schemas import UserCreate, UserResponse
from app.auth  import hash_password

router = APIRouter(
    prefix  = "/auth",
    tags = ["Authentication"]

)
#---------------------------
# DB Dependency
#---------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

#--------------------------
# Signup Endpoint    
#--------------------------    


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    #Check if user already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )
    #hash password
    hashed_pw = hash_password(user.password)

    #create user
    new_user = models.User(
        email = user.email,
        password_hash = hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

