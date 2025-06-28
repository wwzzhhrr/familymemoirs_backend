import os
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def get_email_config() -> Dict[str, Any]:
    """获取邮件服务配置"""
    access_key_id = os.getenv('ALIBABA_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIBABA_ACCESS_KEY_SECRET')
    
    if not access_key_id or not access_key_secret:
        raise ValueError("邮件服务配置缺失：请在环境变量中设置 ALIBABA_ACCESS_KEY_ID 和 ALIBABA_ACCESS_KEY_SECRET")
    
    return {
        'access_key_id': access_key_id,
        'access_key_secret': access_key_secret,
        'endpoint': os.getenv('ALIBABA_EMAIL_ENDPOINT', 'dm.aliyuncs.com'),
        'account_name': os.getenv('EMAIL_ACCOUNT_NAME'),
        'template_path': os.getenv('EMAIL_TEMPLATE_PATH', 'mail_body.html')
    }


def get_redis_config() -> Dict[str, Any]:
    """获取Redis配置"""
    return {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': int(os.getenv('REDIS_PORT', '6379')),
        'db': int(os.getenv('REDIS_DB', '0')),
        'expiry_seconds': int(os.getenv('VERIFICATION_CODE_EXPIRY', '300'))
    }


def get_app_config() -> Dict[str, Any]:
    """获取应用配置"""
    return {
        'debug': os.getenv('DEBUG', 'False').lower() == 'true',
        'host': os.getenv('HOST', '0.0.0.0'),
        'port': int(os.getenv('PORT', '8000')),
        'log_level': os.getenv('LOG_LEVEL', 'INFO')
    }