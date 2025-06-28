import logging
import sys
from typing import Optional
from config.settings import get_app_config


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    设置并返回配置好的日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别，如果不提供则从配置中读取
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    config = get_app_config()
    log_level = level or config['log_level']
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 如果已经有处理器，则不重复添加
    if not logger.handlers:
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器的便捷方法
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器
    """
    return setup_logger(name)