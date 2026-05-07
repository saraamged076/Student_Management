from sqlalchemy.orm import Session
from app.models.models import User, Student
from app.schemas.schemas import UserCreate, StudentCreate, StudentUpdate
from app.auth import verify_password, hash_password

def create_user(db: Session, user_data: UserCreate):

    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        return None

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pw,
        role=user_data.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
 
 # ---------------- STUDENT SERVICES ----------------
def create_student(
    db: Session,
    student_data: StudentCreate,
    owner_id: int
):
    student = Student(
        name=student_data.name,
        department=student_data.department,
        gpa=student_data.gpa,
        owner_id=owner_id
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_students(db: Session):
    return db.query(Student).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(
        Student.id == student_id
    ).first()


def delete_student(db: Session, student_id: int):

    student = get_student_by_id(db, student_id)

    if not student:
        return None

    db.delete(student)
    db.commit()

    return student

def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate
):

    student = get_student_by_id(db, student_id)

    if not student:
        return None

    student.name = student_data.name
    student.department = student_data.department
    student.gpa = student_data.gpa

    db.commit()
    db.refresh(student)

    return student