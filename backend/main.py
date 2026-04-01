from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import PredictRequest, PredictResponse, OptionsResponse
from model import predict_salary, POSITIONS, EDUCATIONS, CITIES, COMPANY_SIZES, INDUSTRIES

app = FastAPI(
    title="AI 薪资预测系统 API",
    description="基于机器学习的薪资预测接口，支持多维度输入",
    version="1.0.0"
)

# 跨域配置（开发阶段允许所有来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="健康检查")
def root():
    return {"status": "running", "message": "AI 薪资预测系统正常运行 🚀"}

@app.get("/api/options", response_model=OptionsResponse, summary="获取下拉选项")
def get_options():
    return {
        "positions": POSITIONS,
        "educations": EDUCATIONS,
        "cities": CITIES,
        "company_sizes": COMPANY_SIZES,
        "industries": INDUSTRIES
    }

@app.post("/api/predict", response_model=PredictResponse, summary="薪资预测")
def predict(req: PredictRequest):
    try:
        result = predict_salary(
            position=req.position,
            education=req.education,
            city=req.city,
            company_size=req.company_size,
            industry=req.industry,
            experience=req.experience
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")

@app.get("/api/stats", summary="模型统计信息")
def get_stats():
    return {
        "model_type": "GradientBoostingRegressor",
        "features": ["职位", "学历", "城市", "公司规模", "行业", "工作年限"],
        "training_samples": 5000,
        "r2_score": "~0.96",
        "supported_positions": len(POSITIONS),
        "supported_cities": len(CITIES)
    }
