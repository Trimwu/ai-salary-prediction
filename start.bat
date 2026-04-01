@echo off
chcp 65001 > nul
echo 🚀 启动 AI 薪资预测系统...

echo 📦 安装后端依赖...
cd backend
pip install -r requirements.txt -q
echo ⚡ 启动 FastAPI 后端...
start "Backend" cmd /k "uvicorn main:app --host 0.0.0.0 --port 8100 --reload"
cd ..

timeout /t 3 /nobreak > nul

echo 🎨 安装前端依赖...
cd frontend
call npm install -q
echo 🌐 启动 Vue3 前端...
start "Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ✅ 系统已启动！
echo    前端地址: http://localhost:5173
echo    后端地址: http://localhost:8100
echo    API 文档: http://localhost:8100/docs
pause
