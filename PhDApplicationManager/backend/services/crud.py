from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

# 修改导入方式
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import models, schemas

# 学校CRUD操作
def create_school(db: Session, school: schemas.SchoolCreate) -> models.School:
    db_school = models.School(**school.model_dump())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

def get_school(db: Session, school_id: int) -> Optional[models.School]:
    return db.query(models.School).filter(models.School.id == school_id).first()

def get_schools(db: Session, skip: int = 0, limit: int = 100) -> List[models.School]:
    return db.query(models.School).offset(skip).limit(limit).all()

def update_school(db: Session, school_id: int, school_data: Dict[str, Any]) -> Optional[models.School]:
    db_school = get_school(db, school_id)
    if db_school:
        for key, value in school_data.items():
            setattr(db_school, key, value)
        db.commit()
        db.refresh(db_school)
    return db_school

def delete_school(db: Session, school_id: int) -> bool:
    db_school = get_school(db, school_id)
    if db_school:
        db.delete(db_school)
        db.commit()
        return True
    return False

# 导师CRUD操作
def create_professor(db: Session, professor: schemas.ProfessorCreate) -> models.Professor:
    db_professor = models.Professor(**professor.model_dump())
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def get_professor(db: Session, professor_id: int) -> Optional[models.Professor]:
    return db.query(models.Professor).filter(models.Professor.id == professor_id).first()

def get_professors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Professor]:
    return db.query(models.Professor).offset(skip).limit(limit).all()

def update_professor(db: Session, professor_id: int, professor_data: Dict[str, Any]) -> Optional[models.Professor]:
    db_professor = get_professor(db, professor_id)
    if db_professor:
        for key, value in professor_data.items():
            setattr(db_professor, key, value)
        db.commit()
        db.refresh(db_professor)
    return db_professor

def delete_professor(db: Session, professor_id: int) -> bool:
    db_professor = get_professor(db, professor_id)
    if db_professor:
        db.delete(db_professor)
        db.commit()
        return True
    return False

# 申请记录CRUD操作
def create_application(db: Session, application: schemas.ApplicationCreate) -> models.Application:
    db_application = models.Application(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application(db: Session, application_id: int) -> Optional[models.Application]:
    return db.query(models.Application).filter(models.Application.id == application_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 100) -> List[models.Application]:
    return db.query(models.Application).offset(skip).limit(limit).all()

def update_application(db: Session, application_id: int, application_data: Dict[str, Any]) -> Optional[models.Application]:
    db_application = get_application(db, application_id)
    if db_application:
        for key, value in application_data.items():
            setattr(db_application, key, value)
        db_application.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_application)
    return db_application

def delete_application(db: Session, application_id: int) -> bool:
    db_application = get_application(db, application_id)
    if db_application:
        db.delete(db_application)
        db.commit()
        return True
    return False

# 文档CRUD操作
def create_document(db: Session, document: schemas.DocumentCreate) -> models.Document:
    db_document = models.Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: int) -> Optional[models.Document]:
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def get_documents(db: Session, application_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[models.Document]:
    query = db.query(models.Document)
    if application_id:
        query = query.filter(models.Document.application_id == application_id)
    return query.offset(skip).limit(limit).all()

def delete_document(db: Session, document_id: int) -> bool:
    db_document = get_document(db, document_id)
    if db_document:
        db.delete(db_document)
        db.commit()
        return True
    return False

# 邮件CRUD操作
def create_email(db: Session, email: schemas.EmailCreate) -> models.Email:
    db_email = models.Email(**email.model_dump())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def get_email(db: Session, email_id: int) -> Optional[models.Email]:
    return db.query(models.Email).filter(models.Email.id == email_id).first()

def get_emails(db: Session, application_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[models.Email]:
    query = db.query(models.Email)
    if application_id:
        query = query.filter(models.Email.application_id == application_id)
    return query.offset(skip).limit(limit).all()

def update_email(db: Session, email_id: int, is_sent: bool = True) -> Optional[models.Email]:
    db_email = get_email(db, email_id)
    if db_email:
        db_email.is_sent = is_sent
        db_email.sent_at = datetime.utcnow()
        db.commit()
        db.refresh(db_email)
    return db_email

def delete_email(db: Session, email_id: int) -> bool:
    db_email = get_email(db, email_id)
    if db_email:
        db.delete(db_email)
        db.commit()
        return True
    return False

# 通知CRUD操作
def create_notification(db: Session, notification: schemas.NotificationCreate) -> models.Notification:
    db_notification = models.Notification(**notification.model_dump())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notification(db: Session, notification_id: int) -> Optional[models.Notification]:
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()

def get_notifications(db: Session, is_read: Optional[bool] = None, skip: int = 0, limit: int = 100) -> List[models.Notification]:
    query = db.query(models.Notification)
    if is_read is not None:
        query = query.filter(models.Notification.is_read == is_read)
    return query.order_by(models.Notification.created_at.desc()).offset(skip).limit(limit).all()

def mark_notification_read(db: Session, notification_id: int, is_read: bool = True) -> Optional[models.Notification]:
    db_notification = get_notification(db, notification_id)
    if db_notification:
        db_notification.is_read = is_read
        db.commit()
        db.refresh(db_notification)
    return db_notification

def delete_notification(db: Session, notification_id: int) -> bool:
    db_notification = get_notification(db, notification_id)
    if db_notification:
        db.delete(db_notification)
        db.commit()
        return True
    return False 