### **AI Salary Predictor — 这是一个基于机器学习的智能薪资预测系统，旨在通过多维度职场数据（职位、城市、学历、经验等）为求职者和招聘方提供精准的薪资参考。**

---

# **AI 薪资预测系统 (AI Salary Predictor)**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue3](https://img.shields.io/badge/Frontend-Vue3-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Scikit-learn](https://img.shields.io/badge/ML-Scikit--learn-F7931E?style=flat-square&logo=scikit-learn)](https://scikit-learn.org/)
[![Element Plus](https://img.shields.io/badge/UI-Element--Plus-409EFF?style=flat-square&logo=element-plus)](https://element-plus.org/)

本系统是一个全栈工程化实践项目，集成了**机器学习模型训练、高性能异步 API 开发以及现代化响应式前端界面**。后端采用 Python 梯度提升回归算法（Gradient Boosting）进行预测，前端基于 Vue3 + Element Plus 构建了极具科技感的交互页面。

## **🌟 项目亮点**

* **全栈架构**：完整的前后端分离架构，涵盖从模型训练到 Web 服务部署的全流程。
* **智能预测**：基于 `Scikit-learn` 的回归模型，支持职位、学历、城市、公司规模、行业及工作年限 6 个维度的加权分析。
* **高性能后端**：利用 `FastAPI` 的异步特性，提供极快的响应速度与自动生成的 Swagger 接口文档。
* **极致 UI 体验**：前端采用深色系科技感设计，包含动态背景、平滑过渡动画及响应式布局，适配多种屏幕尺寸。
* **工程化实践**：严格的 Pydantic 数据校验、Axios 模块化封装、Vue3 组件化开发。

---

## **🛠️ 技术栈**

### **后端 (Python)**

* **框架**: [FastAPI](https://fastapi.tiangolo.com/) (高性能异步 Web 框架)
* **算法**: [Scikit-learn](https://scikit-learn.org/) (GradientBoostingRegressor 梯度提升回归)
* **数据处理**: Pandas, NumPy
* **模型持久化**: Joblib
* **数据校验**: Pydantic

### **前端 (Vue3)**

* **框架**: Vue 3 (Composition API)
* **构建工具**: [Vite](https://vitejs.dev/)
* **UI 组件库**: [Element Plus](https://element-plus.org/)
* **网络请求**: Axios
* **图标库**: @element-plus/icons-vue

---

## **🚀 快速启动**

### **1. 环境准备**

* Python 3.10+
* Node.js 18+ & npm/pnpm

### **2. 一键运行**

项目根目录下提供了自动化脚本，可自动安装依赖并启动服务。

**Windows 用户:**

```bash
start.bat
```

**Linux / Mac 用户:**

```bash
chmod +x start.sh
./start.sh
```

### **3. 手动启动（可选）**

**后端:**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**前端:**

```bash
cd frontend
npm install
npm run dev
```

---

## **📂 目录结构**

```text
salary-prediction/
├── backend/                # Python 后端服务
│   ├── main.py             # API 路由与应用入口
│   ├── model.py            # 机器学习模型训练与预测逻辑
│   ├── schemas.py          # Pydantic 模型定义
│   └── requirements.txt    # 后端依赖列表
├── frontend/               # Vue3 前端应用
│   ├── src/
│   │   ├── api/            # 接口请求封装
│   │   ├── components/     # 可复用组件 (PredictForm 等)
│   │   └── App.vue         # 核心布局与状态管理
│   └── vite.config.js      # Vite 配置与反向代理
└── start.sh                # 跨平台一键启动脚本
```

---

## **📊 机器学习模型说明**

本系统目前内置了一个基于 5000 条模拟职场数据的回归模型。

* **特征工程**：对类别特征（城市、职位等）进行 Label Encoding 处理。
* **模型表现**：Gradient Boosting 算法在该数据集上表现优异，R² 评分接近 0.96。
* **预测逻辑**：系统不仅提供单一预测值，还会根据模型置信区间计算出合理的薪资范围（±15%）。

---

## **⚖️ 开源协议**

本项目遵循 [MIT License](LICENSE) 协议。
