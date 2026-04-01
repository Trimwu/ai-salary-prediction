import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

MODEL_PATH = "salary_model.pkl"
ENCODERS_PATH = "encoders.pkl"

# 职位、学历、城市枚举（前端下拉选项同步使用）
POSITIONS = ["前端工程师", "后端工程师", "算法工程师", "数据分析师", "产品经理",
             "UI设计师", "运维工程师", "测试工程师", "全栈工程师", "架构师"]
EDUCATIONS = ["大专", "本科", "硕士", "博士"]
CITIES = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "西安", "重庆"]
COMPANY_SIZES = ["初创(<50人)", "中小型(50-500人)", "中大型(500-2000人)", "大型(>2000人)"]
INDUSTRIES = ["互联网", "金融科技", "电子商务", "人工智能", "游戏", "医疗健康", "教育", "企业服务"]

def generate_training_data(n=5000):
    """生成模拟训练数据（真实项目可替换为真实数据集）"""
    np.random.seed(42)
    data = []
    for _ in range(n):
        pos_idx = np.random.randint(0, len(POSITIONS))
        edu_idx = np.random.randint(0, len(EDUCATIONS))
        city_idx = np.random.randint(0, len(CITIES))
        size_idx = np.random.randint(0, len(COMPANY_SIZES))
        industry_idx = np.random.randint(0, len(INDUSTRIES))
        exp = np.random.randint(0, 16)

        # 基础薪资逻辑（模拟真实规律）
        base = 8000
        base += [6000, 10000, 8000, 9000, 11000, 5000, 7000, 6000, 12000, 15000][pos_idx]
        base += [0, 3000, 8000, 15000][edu_idx]
        base += [8000, 9000, 6000, 8000, 7000, 5000, 5000, 6000, 5000, 5000][city_idx]
        base += [0, 3000, 7000, 12000][size_idx]
        base += [5000, 8000, 4000, 9000, 6000, 5000, 4000, 6000][industry_idx]
        base += exp * 1500
        # 加入噪声
        salary = base + np.random.normal(0, 3000)
        salary = max(4000, salary)
        data.append([pos_idx, edu_idx, city_idx, size_idx, industry_idx, exp, round(salary, 0)])

    df = pd.DataFrame(data, columns=["position", "education", "city", "company_size", "industry", "experience", "salary"])
    return df

def train_model():
    df = generate_training_data()
    X = df.drop("salary", axis=1)
    y = df["salary"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"✅ 模型训练完成 | R² Score: {r2:.4f} | MAE: {mae:.2f}")

    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    if not os.path.exists(MODEL_PATH):
        print("📦 首次运行，正在训练模型...")
        return train_model()
    return joblib.load(MODEL_PATH)

def predict_salary(position: str, education: str, city: str,
                   company_size: str, industry: str, experience: int) -> dict:
    model = load_model()
    pos_idx = POSITIONS.index(position)
    edu_idx = EDUCATIONS.index(education)
    city_idx = CITIES.index(city)
    size_idx = COMPANY_SIZES.index(company_size)
    ind_idx = INDUSTRIES.index(industry)

    features = np.array([[pos_idx, edu_idx, city_idx, size_idx, ind_idx, experience]])
    predicted = model.predict(features)[0]

    # 生成薪资区间（±15%）
    low = round(predicted * 0.85 / 100) * 100
    high = round(predicted * 1.15 / 100) * 100

    return {
        "predicted_salary": round(predicted, 0),
        "salary_range": {"low": low, "high": high},
        "monthly_salary": round(predicted / 12, 0),
        "level": get_salary_level(predicted)
    }

def get_salary_level(salary):
    if salary < 100000: return {"label": "初级", "color": "#67C23A"}
    elif salary < 200000: return {"label": "中级", "color": "#409EFF"}
    elif salary < 350000: return {"label": "高级", "color": "#E6A23C"}
    else: return {"label": "专家级", "color": "#F56C6C"}
