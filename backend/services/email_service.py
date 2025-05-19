import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Dict, Optional, Any
import os
import json
from datetime import datetime

class EmailService:
    """邮件服务，负责发送和管理邮件"""
    
    def __init__(
        self, 
        smtp_server: str = "smtp.gmail.com", 
        smtp_port: int = 587, 
        username: Optional[str] = None, 
        password: Optional[str] = None
    ):
        """
        初始化邮件服务
        
        Args:
            smtp_server: SMTP服务器地址
            smtp_port: SMTP服务器端口
            username: 邮箱用户名
            password: 邮箱密码或应用密码
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        
    def setup_email_account(self, username: str, password: str) -> bool:
        """
        设置邮箱账户
        
        Args:
            username: 邮箱用户名
            password: 邮箱密码或应用密码
        
        Returns:
            bool: 设置是否成功
        """
        self.username = username
        self.password = password
        
        # 验证凭据是否有效
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.quit()
            return True
        except Exception as e:
            print(f"Email account setup failed: {str(e)}")
            return False
    
    def send_email(
        self, 
        subject: str, 
        body: str, 
        to_email: str, 
        attachments: List[str] = None,
        cc: List[str] = None,
        bcc: List[str] = None
    ) -> Dict[str, Any]:
        """
        发送邮件
        
        Args:
            subject: 邮件主题
            body: 邮件正文
            to_email: 收件人邮箱
            attachments: 附件路径列表
            cc: 抄送邮箱列表
            bcc: 密送邮箱列表
        
        Returns:
            dict: 包含发送状态和消息的字典
        """
        if not self.username or not self.password:
            return {"success": False, "message": "Email account not setup"}
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ", ".join(cc)
            if bcc:
                msg['Bcc'] = ", ".join(bcc)
            
            msg.attach(MIMEText(body, 'plain'))
            
            # 添加附件
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        with open(attachment_path, 'rb') as file:
                            part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                        msg.attach(part)
            
            # 发送邮件
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            server.sendmail(self.username, recipients, msg.as_string())
            server.quit()
            
            return {
                "success": True, 
                "message": "Email sent successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def generate_email_template(self, template_type: str, data: Dict[str, Any]) -> str:
        """
        根据模板类型和数据生成邮件内容
        
        Args:
            template_type: 模板类型，如"初次联系"、"申请跟进"等
            data: 填充模板的数据
        
        Returns:
            str: 生成的邮件内容
        """
        templates = {
            "initial_contact": """
Dear Professor {professor_name},

I am {student_name}, a student with a background in {background}. I am writing to express my interest in pursuing a PhD under your supervision at {school_name}.

I am particularly interested in your research on {research_area}. {custom_message}

I have attached my CV for your consideration. I would be grateful for the opportunity to discuss how my research interests and experience could fit within your group.

Thank you for your time and consideration.

Best regards,
{student_name}
{contact_info}
            """,
            
            "follow_up": """
Dear Professor {professor_name},

I hope this email finds you well. I am writing to follow up on my previous email regarding my interest in joining your research group as a PhD student.

{custom_message}

Thank you again for your time and consideration.

Best regards,
{student_name}
{contact_info}
            """,
            
            "application_status": """
Dear Professor {professor_name},

I hope this email finds you well. I recently submitted my application to the {program_name} program at {school_name}, and I wanted to inform you of my interest in working with you.

{custom_message}

Thank you for your time and consideration.

Best regards,
{student_name}
{contact_info}
            """
        }
        
        template = templates.get(template_type, "")
        
        if template:
            return template.format(**data).strip()
        else:
            return ""
    
    def save_draft(self, draft_data: Dict[str, Any], file_path: str) -> bool:
        """
        保存邮件草稿
        
        Args:
            draft_data: 邮件草稿数据
            file_path: 保存路径
        
        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 添加时间戳
            draft_data["last_modified"] = datetime.utcnow().isoformat()
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(draft_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Failed to save draft: {str(e)}")
            return False
    
    def load_draft(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        加载邮件草稿
        
        Args:
            file_path: 草稿文件路径
        
        Returns:
            Optional[Dict[str, Any]]: 草稿数据，如果加载失败则返回None
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Failed to load draft: {str(e)}")
            return None 