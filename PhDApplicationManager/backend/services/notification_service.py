from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import os
from sqlalchemy.orm import Session

# 修改导入方式
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import models, schemas
from database.database import get_db

class NotificationService:
    """
    通知服务，负责管理和发送系统通知
    """
    
    def __init__(self, db: Optional[Session] = None):
        """
        初始化通知服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def create_notification(
        self, 
        title: str, 
        content: str, 
        notification_type: str,
        db: Optional[Session] = None
    ) -> models.Notification:
        """
        创建新通知
        
        Args:
            title: 通知标题
            content: 通知内容
            notification_type: 通知类型 (例如: "截止日期", "邮件回复", "申请状态变更")
            db: 数据库会话 (可选)
        
        Returns:
            models.Notification: 新创建的通知对象
        """
        _db = db or self.db
        if not _db:
            raise ValueError("Database session is required")
        
        notification_data = schemas.NotificationCreate(
            title=title,
            content=content,
            type=notification_type
        )
        
        db_notification = models.Notification(**notification_data.model_dump())
        _db.add(db_notification)
        _db.commit()
        _db.refresh(db_notification)
        
        return db_notification
    
    def create_deadline_notification(
        self, 
        school_name: str, 
        deadline: datetime,
        days_before: int = 7,
        db: Optional[Session] = None
    ) -> models.Notification:
        """
        创建截止日期提醒通知
        
        Args:
            school_name: 学校名称
            deadline: 截止日期
            days_before: 提前多少天发送通知
            db: 数据库会话 (可选)
        
        Returns:
            models.Notification: 新创建的通知对象
        """
        title = f"{school_name}申请截止日期提醒"
        days_left = (deadline - datetime.utcnow()).days
        
        if days_left <= 0:
            content = f"{school_name}的申请截止日期是今天！请确保已提交申请。"
        else:
            content = f"{school_name}的申请截止日期还有{days_left}天，请及时准备和提交申请。"
        
        return self.create_notification(
            title=title,
            content=content,
            notification_type="截止日期",
            db=db
        )
    
    def create_email_reply_notification(
        self, 
        professor_name: str, 
        email_subject: str,
        db: Optional[Session] = None
    ) -> models.Notification:
        """
        创建邮件回复通知
        
        Args:
            professor_name: 导师姓名
            email_subject: 邮件主题
            db: 数据库会话 (可选)
        
        Returns:
            models.Notification: 新创建的通知对象
        """
        title = f"收到{professor_name}的邮件回复"
        content = f"{professor_name}回复了您的邮件 '{email_subject}'，请及时查看。"
        
        return self.create_notification(
            title=title,
            content=content,
            notification_type="邮件回复",
            db=db
        )
    
    def create_status_change_notification(
        self, 
        school_name: str, 
        old_status: str,
        new_status: str,
        db: Optional[Session] = None
    ) -> models.Notification:
        """
        创建申请状态变更通知
        
        Args:
            school_name: 学校名称
            old_status: 旧状态
            new_status: 新状态
            db: 数据库会话 (可选)
        
        Returns:
            models.Notification: 新创建的通知对象
        """
        title = f"{school_name}申请状态变更"
        content = f"您在{school_name}的申请状态从'{old_status}'变更为'{new_status}'。"
        
        return self.create_notification(
            title=title,
            content=content,
            notification_type="申请状态变更",
            db=db
        )
    
    def check_upcoming_deadlines(self, days_threshold: int = 7, db: Optional[Session] = None) -> List[models.Notification]:
        """
        检查即将到来的截止日期并创建通知
        
        Args:
            days_threshold: 提前多少天发送通知
            db: 数据库会话 (可选)
        
        Returns:
            List[models.Notification]: 创建的通知列表
        """
        _db = db or self.db
        if not _db:
            raise ValueError("Database session is required")
        
        # 获取即将到来的截止日期
        deadline_threshold = datetime.utcnow() + timedelta(days=days_threshold)
        schools_with_deadlines = _db.query(models.School).filter(
            models.School.application_deadline <= deadline_threshold,
            models.School.application_deadline > datetime.utcnow()
        ).all()
        
        notifications = []
        for school in schools_with_deadlines:
            notification = self.create_deadline_notification(
                school_name=school.name,
                deadline=school.application_deadline,
                days_before=days_threshold,
                db=_db
            )
            notifications.append(notification)
        
        return notifications
    
    def get_unread_notifications(self, db: Optional[Session] = None) -> List[models.Notification]:
        """
        获取未读通知
        
        Args:
            db: 数据库会话 (可选)
        
        Returns:
            List[models.Notification]: 未读通知列表
        """
        _db = db or self.db
        if not _db:
            raise ValueError("Database session is required")
        
        return _db.query(models.Notification).filter(models.Notification.is_read == False).order_by(models.Notification.created_at.desc()).all()
    
    def mark_notification_as_read(self, notification_id: int, db: Optional[Session] = None) -> bool:
        """
        将通知标记为已读
        
        Args:
            notification_id: 通知ID
            db: 数据库会话 (可选)
        
        Returns:
            bool: 操作是否成功
        """
        _db = db or self.db
        if not _db:
            raise ValueError("Database session is required")
        
        notification = _db.query(models.Notification).filter(models.Notification.id == notification_id).first()
        if notification:
            notification.is_read = True
            _db.commit()
            return True
        return False

# 可扩展的移动设备通知服务
class MobileNotificationService:
    """
    移动设备通知服务，用于向移动设备发送推送通知
    注意：这是一个示例实现，实际应用中需要集成第三方推送服务
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化移动设备通知服务
        
        Args:
            api_key: 推送服务API密钥
        """
        self.api_key = api_key
        self.devices = []  # 存储已注册的设备
    
    def register_device(self, device_token: str, device_type: str) -> bool:
        """
        注册设备
        
        Args:
            device_token: 设备令牌
            device_type: 设备类型 (例如: "ios", "android")
        
        Returns:
            bool: 注册是否成功
        """
        self.devices.append({
            "token": device_token,
            "type": device_type,
            "registered_at": datetime.utcnow().isoformat()
        })
        return True
    
    def send_push_notification(self, title: str, message: str, device_tokens: List[str] = None) -> Dict[str, Any]:
        """
        发送推送通知
        
        Args:
            title: 通知标题
            message: 通知内容
            device_tokens: 设备令牌列表，如果为None则发送给所有已注册设备
        
        Returns:
            Dict[str, Any]: 发送结果
        """
        # 这是一个示例实现，实际应用中需要集成第三方推送服务
        # 例如Firebase Cloud Messaging或Apple Push Notification Service
        
        if not device_tokens:
            device_tokens = [device["token"] for device in self.devices]
        
        # 模拟发送通知
        result = {
            "success": True,
            "sent_to": len(device_tokens),
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"Notification '{title}' sent successfully"
        }
        
        return result 