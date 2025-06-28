import traceback
import redis
from fastapi import FastAPI, HTTPException
from .services.email_service import EmailService
from .services.verification_service import VerificationService
from .models.email_models import EmailRequest, VerifyCodeRequest, EmailResponse, VerifyCodeResponse
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="邮件验证码服务",
    description="基于FastAPI的邮件验证码发送和验证服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 使用try-except包装服务初始化，以捕获可能的初始化错误
try:
    email_service = EmailService()
    logger.info("Email service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize email service: {str(e)}")
    logger.error(traceback.format_exc())
    raise

try:
    # 可以从环境变量或配置文件中读取这些值
    verification_service = VerificationService(
        redis_host='localhost',  # 默认值，可以根据需要修改
        redis_port=6379,         # 默认值，可以根据需要修改
        redis_db=0,
        expiry_seconds=300       # 5分钟过期
    )
    logger.info("验证服务初始化成功")
except redis.ConnectionError as e:
    logger.error(f"Redis连接错误: {str(e)}")
    logger.error("请确保Redis服务器正在运行，或者修改连接参数")
    logger.error(traceback.format_exc())
    raise
except Exception as e:
    logger.error(f"初始化验证服务失败: {str(e)}")
    logger.error(traceback.format_exc())
    raise





@app.post("/mail/send-verification-code")
def send_verification_code(request: EmailRequest):
    """发送验证码邮件"""
    try:
        # 生成随机验证码并存储
        logger.info(f"正在为邮箱 {request.to_address} 生成验证码")
        try:
            code = verification_service.generate_code(request.to_address)
            logger.info(f"验证码生成成功: {code}")
        except Exception as e:
            logger.error(f"生成验证码失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise

        logger.info(f"正在发送验证码邮件到 {request.to_address}")
        try:
            result = email_service.send_verification_email(
                to_address=request.to_address,
                code=code,
                subject=request.subject,
                from_alias=request.from_alias
            )
            logger.info(f"邮件发送结果: {result}")
        except Exception as e:
            logger.error(f"发送邮件失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise

        return {"message": "验证码已发送", "email": request.to_address}
    except ValueError as e:
        logger.error(f"值错误: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))
    except IOError as e:
        logger.error(f"IO错误: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"未预期的错误: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail={"error": str(e), "type": type(e).__name__})


@app.post("/mail/verify-code")
def verify_code(request: VerifyCodeRequest):
    """验证验证码是否正确"""
    try:
        is_valid = verification_service.verify_code(request.address, request.code)
        if is_valid:
            return {"message": "验证成功", "valid": True}
        else:
            raise HTTPException(status_code=400, detail="验证码无效或已过期")
    except Exception as e:
        logger.error(f"验证码验证失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "邮件验证码服务已启动", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "邮件验证码服务", "version": "1.0.0"}

@app.get("/mail/health")
def mail_health_check():
    return {"status": "healthy", "module": "邮件服务", "features": ["发送验证码", "验证验证码"]}