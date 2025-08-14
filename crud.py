from sqlalchemy.orm import Session
import uuid

from . import models, schemas, auth

# --- User CRUD ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- License CRUD ---
def generate_license_key() -> str:
    return str(uuid.uuid4())

def create_user_license(db: Session, license: schemas.LicenseCreate):
    new_key = generate_license_key()
    db_license = models.License(key=new_key, owner_id=license.owner_id)
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

def get_license_by_key(db: Session, key: str):
    return db.query(models.License).filter(models.License.key == key).first()