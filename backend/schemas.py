from pydantic import BaseModel, Field
from typing import Optional

class PredictRequest(BaseModel):
    position: str = Field(..., description="职位名称")
    education: str = Field(..., description="学历")
    city: str = Field(..., description="城市")
    company_size: str = Field(..., description="公司规模")
    industry: str = Field(..., description="行业")
    experience: int = Field(..., ge=0, le=30, description="工作年限")

class SalaryLevel(BaseModel):
    label: str
    color: str

class SalaryRange(BaseModel):
    low: float
    high: float

class PredictResponse(BaseModel):
    predicted_salary: float
    salary_range: SalaryRange
    monthly_salary: float
    level: SalaryLevel

class OptionsResponse(BaseModel):
    positions: list[str]
    educations: list[str]
    cities: list[str]
    company_sizes: list[str]
    industries: list[str]
