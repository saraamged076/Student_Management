from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.logging_config import logger
from app.database import get_db
from app.models.models import User
from app.auth import get_current_user
from app.redis_client import redis_client
from app.monitoring import metrics
import json

from app.schemas.schemas import (
    StudentCreate,
    StudentResponse,
    StudentUpdate
)

from app.services.services import (
    create_student,
    get_students,
    get_student_by_id,
    delete_student,
    update_student,
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/", response_model=StudentResponse)
def create_new_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    metrics["total_requests"] += 1

    student = create_student(
        db,
        student_data,
        current_user.id
    )

    # clear cache
    redis_client.delete("students")
    redis_client.delete(f"student:{student.id}")

    logger.info(
        f"Student created: {student.name} by user {current_user.username}"
    )

    return student


@router.get("/", response_model=list[StudentResponse])
def get_all_students(
    db: Session = Depends(get_db)
):

    metrics["total_requests"] += 1

    # check cache
    cached_students = redis_client.get("students")

    if cached_students:

        metrics["cache_hits"] += 1

        print("Data from Redis Cache")
        return json.loads(cached_students)

    # get from database
    students = get_students(db)

    # save in cache
    redis_client.set(
        "students",
        json.dumps(
            [
                {
                    "id": s.id,
                    "name": s.name,
                    "department": s.department,
                    "gpa": s.gpa,
                    "owner_id": s.owner_id,
                }
                for s in students
            ]
        ),
        ex=60,
    )

    print("Data from Database")

    return students


@router.get("/{student_id}", response_model=StudentResponse)
def get_single_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    metrics["total_requests"] += 1

    cache_key = f"student:{student_id}"

    # check cache
    cached_student = redis_client.get(cache_key)

    if cached_student:

        metrics["cache_hits"] += 1

        print("Single Student from Redis Cache")
        return json.loads(cached_student)

    # get from database
    student = get_student_by_id(
        db,
        student_id
    )

    if not student:

        metrics["errors"] += 1

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # save to cache
    redis_client.set(
        cache_key,
        json.dumps(
            {
                "id": student.id,
                "name": student.name,
                "department": student.department,
                "gpa": student.gpa,
                "owner_id": student.owner_id
            }
        ),
        ex=60
    )

    print("Single Student from Database")

    return student


@router.delete("/{student_id}")
def remove_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    metrics["total_requests"] += 1

    student = get_student_by_id(db, student_id)

    if not student:

        metrics["errors"] += 1

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # only admin can delete
    if current_user.role != "admin":

        metrics["errors"] += 1

        raise HTTPException(
            status_code=403,
            detail="Only admins can delete students"
        )

    delete_student(db, student_id)

    # clear cache
    redis_client.delete("students")
    redis_client.delete(f"student:{student_id}")

    logger.warning(
        f"Student deleted: ID {student_id} by admin {current_user.username}"
    )

    return {
        "message": "Student deleted successfully"
    }


@router.put("/{student_id}", response_model=StudentResponse)
def edit_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    metrics["total_requests"] += 1

    student = get_student_by_id(db, student_id)

    if not student:

        metrics["errors"] += 1

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # owner or admin only
    if (
        student.owner_id != current_user.id
        and current_user.role != "admin"
    ):

        metrics["errors"] += 1

        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this student"
        )

    updated_student = update_student(
        db,
        student_id,
        student_data
    )

    # clear cache
    redis_client.delete("students")
    redis_client.delete(f"student:{student_id}")

    logger.info(
        f"Student updated: {updated_student.name} by user {current_user.username}"
    )

    return updated_student