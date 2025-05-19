from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

# 修改导入方式
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import Base

# 学校与导师多对多关系的关联表
school_professor = Table(
    "school_professor",
    Base.metadata,
    Column("school_id", Integer, ForeignKey("schools.id"), primary_key=True),
    Column("professor_id", Integer, ForeignKey("professors.id"), primary_key=True),
)

class School(Base):
    """学校模型"""
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String)
    program = Column(String)
    location = Column(String)
    website = Column(String)
    application_start = Column(DateTime, nullable=True)
    application_deadline = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    # 关系
    professors = relationship("Professor", secondary=school_professor, back_populates="schools")
    applications = relationship("Application", back_populates="school")

class Professor(Base):
    """导师模型"""
    __tablename__ = "professors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    research_area = Column(String)
    website = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # 关系
    schools = relationship("School", secondary=school_professor, back_populates="professors")
    applications = relationship("Application", back_populates="professor")

class Application(Base):
    """申请记录模型"""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=True)
    status = Column(String)  # 例如: "准备中", "已提交", "已面试", "录取", "拒绝"
    submission_date = Column(DateTime, nullable=True)
    result_date = Column(DateTime, nullable=True)
    cv_path = Column(String, nullable=True)
    ps_path = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    school = relationship("School", back_populates="applications")
    professor = relationship("Professor", back_populates="applications")
    documents = relationship("Document", back_populates="application")
    emails = relationship("Email", back_populates="application")

class Document(Base):
    """文档模型，用于存储申请相关的文件"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String)
    type = Column(String)  # 例如: "CV", "个人陈述", "推荐信", "成绩单"
    path = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    application = relationship("Application", back_populates="documents")

class Email(Base):
    """邮件模型，用于跟踪与导师或学校的通信"""
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    subject = Column(String)
    content = Column(Text)
    sender = Column(String)
    receiver = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    is_sent = Column(Boolean, default=False)
    
    # 关系
    application = relationship("Application", back_populates="emails")

class Notification(Base):
    """通知模型，用于发送消息提醒"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    type = Column(String)  # 例如: "截止日期", "邮件回复", "申请状态变更"
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow) 