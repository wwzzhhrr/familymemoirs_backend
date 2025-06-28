#!/usr/bin/env python3
"""
邮件验证码服务主入口文件
"""

import uvicorn
from app.main import app
from config.settings import get_app_config
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """应用程序主入口"""
    config = get_app_config()
    
    logger.info("正在启动邮件验证码服务...")
    logger.info(f"配置信息: Host={config['host']}, Port={config['port']}, Debug={config['debug']}")
    
    uvicorn.run(
        "app.main:app",
        host=config['host'],
        port=config['port'],
        reload=config['debug'],
        log_level=config['log_level'].lower()
    )


if __name__ == "__main__":
    main()


