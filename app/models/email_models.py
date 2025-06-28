from pydantic import BaseModel, EmailStr
from typing import Optional


class EmailRequest(BaseModel):
    """邮件发送请求模型"""
    to_address: EmailStr
    subject: Optional[str] = "验证码通知"
    from_alias: Optional[str] = "家书万金"


class VerifyCodeRequest(BaseModel):
    """验证码验证请求模型"""
    address: EmailStr
    code: str


class EmailResponse(BaseModel):
    """邮件发送响应模型"""
    message: str
    email: str


class VerifyCodeResponse(BaseModel):
    """验证码验证响应模型"""
    message: str
    valid: bool