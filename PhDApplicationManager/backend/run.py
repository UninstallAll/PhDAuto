import uvicorn
import os
import sys

# 添加当前目录到PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    # 启动FastAPI应用
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True) 