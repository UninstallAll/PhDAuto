from database.database import engine
from models.models import Base

def init_database():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成！表已创建。")

if __name__ == "__main__":
    init_database() 