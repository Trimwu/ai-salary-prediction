#!/bin/bash
echo "🚀 启动 AI 薪资预测系统..."

# 启动后端
echo "📦 安装后端依赖..."
cd backend
pip install -r requirements.txt -q
echo "⚡ 启动 FastAPI 后端 (port 8100)..."
uvicorn main:app --host 0.0.0.0 --port 8100 --reload &
BACKEND_PID=$!
cd ..

# 等待后端就绪
sleep 3

# 启动前端
echo "🎨 安装前端依赖..."
cd frontend
npm install -q
echo "🌐 启动 Vue3 前端 (port 5173)..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 系统已启动！"
echo "   前端地址: http://localhost:5173"
echo "   后端地址: http://localhost:8100"
echo "   API 文档: http://localhost:8100/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 捕获退出信号
trap "kill $BACKEND_PID $FRONTEND_PID; echo '已停止所有服务'" EXIT
wait
