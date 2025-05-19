from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import List, Optional

# 学校相关模型
class SchoolBase(BaseModel):
    name: str
    department: Optional[str] = None
    program: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    application_start: Optional[datetime] = None
    application_deadline: Optional[datetime] = None
    notes: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    id: int
    
    class Config:
        from_attributes = True

# 导师相关模型
class ProfessorBase(BaseModel):
    name: str
    email: str
    research_area: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int
    
    class Config:
        from_attributes = True

# 申请记录相关模型
class ApplicationBase(BaseModel):
    school_id: int
    professor_id: Optional[int] = None
    status: str = "准备中"
    submission_date: Optional[datetime] = None
    result_date: Optional[datetime] = None
    cv_path: Optional[str] = None
    ps_path: Optional[str] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    submission_date: Optional[datetime] = None
    result_date: Optional[datetime] = None
    cv_path: Optional[str] = None
    ps_path: Optional[str] = None
    notes: Optional[str] = None

class Application(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 文档相关模型
class DocumentBase(BaseModel):
    application_id: int
    name: str
    type: str
    path: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# 邮件相关模型
class EmailBase(BaseModel):
    application_id: int
    subject: str
    content: str
    sender: str
    receiver: str
    is_sent: bool = False

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    sent_at: datetime
    
    class Config:
        from_attributes = True

# 通知相关模型
class NotificationBase(BaseModel):
    title: str
    content: str
    type: str
    is_read: bool = False

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 包含关系的扩展模型
class SchoolWithRelations(School):
    professors: List[Professor] = []
    applications: List[Application] = []

class ProfessorWithRelations(Professor):
    schools: List[School] = []
    applications: List[Application] = []

class ApplicationWithRelations(Application):
    school: School
    professor: Optional[Professor] = None
    documents: List[Document] = []
    emails: List[Email] = [] 