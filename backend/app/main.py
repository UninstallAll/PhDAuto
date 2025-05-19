from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Form, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime
import sys

# 修改导入方式
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import engine, Base, get_db
from models import models, schemas
from services import crud, information_retrieval, email_service, notification_service

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="PhD Application Manager",
    description="博士申请管理系统API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为特定的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建服务实例
info_service = information_retrieval.InformationRetrievalService()
email_svc = email_service.EmailService()
notification_svc = notification_service.NotificationService()

# 根路由
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "欢迎使用博士申请管理系统API"}

# 学校相关路由
@app.post("/schools/", response_model=schemas.School, tags=["Schools"])
def create_school(school: schemas.SchoolCreate, db: Session = Depends(get_db)):
    return crud.create_school(db=db, school=school)

@app.get("/schools/", response_model=List[schemas.School], tags=["Schools"])
def read_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schools = crud.get_schools(db, skip=skip, limit=limit)
    return schools

@app.get("/schools/{school_id}", response_model=schemas.School, tags=["Schools"])
def read_school(school_id: int, db: Session = Depends(get_db)):
    db_school = crud.get_school(db, school_id=school_id)
    if db_school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return db_school

@app.put("/schools/{school_id}", response_model=schemas.School, tags=["Schools"])
def update_school(school_id: int, school_data: dict, db: Session = Depends(get_db)):
    db_school = crud.update_school(db, school_id=school_id, school_data=school_data)
    if db_school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return db_school

@app.delete("/schools/{school_id}", tags=["Schools"])
def delete_school(school_id: int, db: Session = Depends(get_db)):
    success = crud.delete_school(db, school_id=school_id)
    if not success:
        raise HTTPException(status_code=404, detail="School not found")
    return {"detail": "School deleted successfully"}

# 导师相关路由
@app.post("/professors/", response_model=schemas.Professor, tags=["Professors"])
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    return crud.create_professor(db=db, professor=professor)

@app.get("/professors/", response_model=List[schemas.Professor], tags=["Professors"])
def read_professors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    professors = crud.get_professors(db, skip=skip, limit=limit)
    return professors

@app.get("/professors/{professor_id}", response_model=schemas.Professor, tags=["Professors"])
def read_professor(professor_id: int, db: Session = Depends(get_db)):
    db_professor = crud.get_professor(db, professor_id=professor_id)
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return db_professor

@app.put("/professors/{professor_id}", response_model=schemas.Professor, tags=["Professors"])
def update_professor(professor_id: int, professor_data: dict, db: Session = Depends(get_db)):
    db_professor = crud.update_professor(db, professor_id=professor_id, professor_data=professor_data)
    if db_professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return db_professor

@app.delete("/professors/{professor_id}", tags=["Professors"])
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    success = crud.delete_professor(db, professor_id=professor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Professor not found")
    return {"detail": "Professor deleted successfully"}

# 申请记录相关路由
@app.post("/applications/", response_model=schemas.Application, tags=["Applications"])
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db=db, application=application)

@app.get("/applications/", response_model=List[schemas.Application], tags=["Applications"])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applications = crud.get_applications(db, skip=skip, limit=limit)
    return applications

@app.get("/applications/{application_id}", response_model=schemas.ApplicationWithRelations, tags=["Applications"])
def read_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@app.put("/applications/{application_id}", response_model=schemas.Application, tags=["Applications"])
def update_application(application_id: int, application_data: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    db_application = crud.update_application(db, application_id=application_id, application_data=application_data.model_dump(exclude_unset=True))
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # 检查状态变更，并创建通知
    if application_data.status and db_application.status != application_data.status:
        school = crud.get_school(db, school_id=db_application.school_id)
        notification_svc.create_status_change_notification(
            school_name=school.name,
            old_status=db_application.status,
            new_status=application_data.status,
            db=db
        )
    
    return db_application

@app.delete("/applications/{application_id}", tags=["Applications"])
def delete_application(application_id: int, db: Session = Depends(get_db)):
    success = crud.delete_application(db, application_id=application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"detail": "Application deleted successfully"}

# 文档相关路由
@app.post("/documents/", response_model=schemas.Document, tags=["Documents"])
async def create_document(
    application_id: int = Form(...),
    name: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 创建文件存储目录
    upload_dir = os.path.join("uploads", "documents", str(application_id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # 创建文档记录
    document = schemas.DocumentCreate(
        application_id=application_id,
        name=name,
        type=document_type,
        path=file_path
    )
    
    return crud.create_document(db=db, document=document)

@app.get("/documents/", response_model=List[schemas.Document], tags=["Documents"])
def read_documents(application_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, application_id=application_id, skip=skip, limit=limit)
    return documents

@app.delete("/documents/{document_id}", tags=["Documents"])
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = crud.get_document(db, document_id=document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # 删除文件
    if os.path.exists(document.path):
        os.remove(document.path)
    
    # 删除数据库记录
    success = crud.delete_document(db, document_id=document_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete document record")
    
    return {"detail": "Document deleted successfully"}

# 邮件相关路由
@app.post("/emails/", response_model=schemas.Email, tags=["Emails"])
def create_email(email: schemas.EmailCreate, db: Session = Depends(get_db)):
    return crud.create_email(db=db, email=email)

@app.get("/emails/", response_model=List[schemas.Email], tags=["Emails"])
def read_emails(application_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emails = crud.get_emails(db, application_id=application_id, skip=skip, limit=limit)
    return emails

@app.post("/emails/{email_id}/send", response_model=schemas.Email, tags=["Emails"])
def send_email(
    email_id: int, 
    smtp_server: str = Body("smtp.gmail.com"), 
    smtp_port: int = Body(587),
    username: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    db_email = crud.get_email(db, email_id=email_id)
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # 设置邮件服务
    email_svc.smtp_server = smtp_server
    email_svc.smtp_port = smtp_port
    email_svc.username = username
    email_svc.password = password
    
    # 发送邮件
    result = email_svc.send_email(
        subject=db_email.subject,
        body=db_email.content,
        to_email=db_email.receiver
    )
    
    if result["success"]:
        # 更新邮件状态
        db_email = crud.update_email(db, email_id=email_id, is_sent=True)
        return db_email
    else:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {result['message']}")

@app.delete("/emails/{email_id}", tags=["Emails"])
def delete_email(email_id: int, db: Session = Depends(get_db)):
    success = crud.delete_email(db, email_id=email_id)
    if not success:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"detail": "Email deleted successfully"}

# 通知相关路由
@app.get("/notifications/", response_model=List[schemas.Notification], tags=["Notifications"])
def read_notifications(is_read: Optional[bool] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = crud.get_notifications(db, is_read=is_read, skip=skip, limit=limit)
    return notifications

@app.put("/notifications/{notification_id}/read", response_model=schemas.Notification, tags=["Notifications"])
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    notification = crud.mark_notification_read(db, notification_id=notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.post("/notifications/check-deadlines", response_model=List[schemas.Notification], tags=["Notifications"])
def check_deadlines(days_threshold: int = Query(7), db: Session = Depends(get_db)):
    notification_service_instance = notification_service.NotificationService(db)
    notifications = notification_service_instance.check_upcoming_deadlines(days_threshold=days_threshold)
    return notifications

# 信息检索路由
@app.get("/search/school", tags=["Search"])
def search_school_info(school_name: str, department: Optional[str] = None):
    return info_service.search_school_info(school_name=school_name, department=department)

@app.get("/search/professor", tags=["Search"])
def search_professor_info(name: str, school: Optional[str] = None):
    return info_service.search_professor_info(name=name, school=school)

@app.get("/search/deadlines", tags=["Search"])
def get_application_deadlines(school_name: str, program: str):
    deadline = info_service.get_application_deadlines(school_name=school_name, program=program)
    if deadline:
        return {"school": school_name, "program": program, "deadline": deadline}
    else:
        return {"school": school_name, "program": program, "deadline": None, "message": "Deadline not found"}

@app.get("/search/publications", tags=["Search"])
def get_professor_publications(professor_name: str, limit: int = 5):
    return info_service.get_professor_publications(professor_name=professor_name, limit=limit)

@app.post("/email/generate-draft", tags=["Email"])
def generate_email_draft(professor_info: dict, student_info: dict):
    email_content = info_service.generate_email_draft(professor_info=professor_info, student_info=student_info)
    return {"subject": f"PhD Application Inquiry - {student_info.get('name')}", "content": email_content}

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 