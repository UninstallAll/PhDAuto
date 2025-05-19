import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import re
import json

class InformationRetrievalService:
    """
    负责从网络获取学校和导师信息的服务
    未来可以集成各种API或AI服务（如DeepSeek）
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    def search_school_info(self, school_name: str, department: Optional[str] = None) -> Dict[str, Any]:
        """
        搜索学校信息
        目前是模拟实现，未来可以接入实际API
        """
        # 这里是模拟实现，实际应用中应该调用外部API或使用网页抓取
        return {
            "name": school_name,
            "department": department or "Computer Science",
            "website": f"https://www.{school_name.lower().replace(' ', '')}.edu",
            "application_deadline": "2023-12-15T00:00:00Z",
            "location": "United States"
        }
    
    def search_professor_info(self, name: str, school: Optional[str] = None) -> Dict[str, Any]:
        """
        搜索导师信息
        目前是模拟实现，未来可以接入实际API
        """
        # 这里是模拟实现，实际应用中应该调用外部API或使用网页抓取
        return {
            "name": name,
            "email": f"{name.lower().replace(' ', '.')}@{school.lower().replace(' ', '')}.edu" if school else "unknown@example.com",
            "research_area": "Artificial Intelligence, Machine Learning",
            "website": f"https://www.{school.lower().replace(' ', '')}.edu/~{name.lower().split()[0]}" if school else None
        }
    
    def get_application_deadlines(self, school_name: str, program: str) -> Optional[datetime]:
        """
        获取申请截止日期
        目前是模拟实现，未来可以接入实际API
        """
        # 这里是模拟实现，实际应用中应该调用外部API或使用网页抓取
        deadlines = {
            "Stanford University": "2023-12-01T00:00:00Z",
            "MIT": "2023-12-15T00:00:00Z",
            "UC Berkeley": "2023-12-05T00:00:00Z",
            "Carnegie Mellon University": "2023-12-10T00:00:00Z",
            "Harvard University": "2023-12-01T00:00:00Z"
        }
        
        return deadlines.get(school_name)
        
    def get_professor_publications(self, professor_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        获取导师的发表论文
        目前是模拟实现，未来可以接入实际API
        """
        # 这里是模拟实现，实际应用中应该调用外部API或使用网页抓取
        return [
            {
                "title": f"Innovative Research in AI by {professor_name}",
                "year": 2023,
                "venue": "ICML",
                "url": "https://example.com/paper1"
            },
            {
                "title": f"Machine Learning Applications by {professor_name}",
                "year": 2022,
                "venue": "NeurIPS",
                "url": "https://example.com/paper2"
            }
        ][:limit]
    
    def generate_email_draft(self, professor_info: Dict[str, Any], student_info: Dict[str, Any]) -> str:
        """
        根据导师和学生信息生成邮件草稿
        目前是模拟实现，未来可以接入AI服务如DeepSeek
        """
        # 这里是模拟实现，实际应用中应该调用AI API
        template = f"""
Subject: PhD Application Inquiry - {student_info.get('name')}

Dear Professor {professor_info.get('name')},

I am {student_info.get('name')}, a student with a background in {student_info.get('background')}. I am interested in pursuing a PhD under your supervision in the field of {professor_info.get('research_area')}.

I have experience in {student_info.get('experience')} and have been working on projects related to {student_info.get('projects')}.

I would appreciate the opportunity to discuss potential research collaborations and your current openings for PhD students.

Thank you for your time and consideration.

Best regards,
{student_info.get('name')}
{student_info.get('contact')}
        """
        
        return template.strip()

# 将来可以添加更多的信息检索服务
class DeepSeekService:
    """
    DeepSeek API集成服务
    注意：这需要有效的DeepSeek API密钥
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def search_information(self, query: str) -> Dict[str, Any]:
        """
        使用DeepSeek搜索信息
        """
        try:
            payload = {
                "query": query,
                "max_tokens": 500
            }
            
            response = requests.post(
                f"{self.api_url}/search",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API request failed with status code {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """
        使用DeepSeek生成内容
        """
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": 1000
            }
            
            response = requests.post(
                f"{self.api_url}/generate",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API request failed with status code {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)} 