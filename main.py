from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from  import crud, models, schemas, auth
from database import SessionLocal, engine

# Lệnh này không còn cần thiết ở đây vì build.sh đã xử lý
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="License Server API")

# Dependency để lấy session CSDL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the License Server API!"}

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token, tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/licenses/", response_model=schemas.License, status_code=status.HTTP_201_CREATED, tags=["Licenses"])
def create_license_for_user_endpoint(license: schemas.LicenseCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=license.owner_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_license(db=db, license=license)

@app.get("/licenses/verify/{key}", tags=["Licenses"])
def verify_license_endpoint(key: str, db: Session = Depends(get_db)):
    db_license = crud.get_license_by_key(db, key=key)
    if db_license and db_license.is_active:
        return {"status": "valid", "license_key": key, "owner_email": db_license.owner.email}
    raise HTTPException(status_code=404, detail="License key not found or inactive")