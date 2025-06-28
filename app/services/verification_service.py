import random
import redis
import logging
from config.settings import get_redis_config

logger = logging.getLogger(__name__)


class VerificationService:
    """验证码服务，用于生成、存储和验证验证码"""
    
    def __init__(self, redis_host: str = None, redis_port: int = None, redis_db: int = None, expiry_seconds: int = None):
        """
        初始化验证码服务
        
        Args:
            redis_host: Redis服务器地址
            redis_port: Redis服务器端口
            redis_db: Redis数据库编号
            expiry_seconds: 验证码过期时间（秒）
        """
        config = get_redis_config()
        
        self.redis_host = redis_host or config['host']
        self.redis_port = redis_port or config['port']
        self.redis_db = redis_db or config['db']
        self.expiry_seconds = expiry_seconds or config['expiry_seconds']
        self.prefix = "verification_code:"
        
        # 初始化Redis客户端
        self.redis_client = self._create_redis_client()
        
    def _create_redis_client(self):
        """创建Redis客户端连接"""
        try:
            client = redis.Redis(
                host=self.redis_host, 
                port=self.redis_port, 
                db=self.redis_db,
                socket_timeout=5,  # 设置超时时间
                socket_connect_timeout=5,
                retry_on_timeout=True,  # 超时时重试
                decode_responses=False  # 不自动解码响应
            )
            # 测试连接
            client.ping()
            logger.info(f"成功连接到Redis服务器: {self.redis_host}:{self.redis_port}")
            return client
        except redis.ConnectionError as e:
            logger.error(f"无法连接到Redis服务器: {str(e)}")
            raise
    
    def generate_code(self, email: str) -> str:
        """
        为指定邮箱生成6位随机验证码并存储到Redis
        
        Args:
            email: 用户邮箱
            
        Returns:
            str: 生成的6位数字验证码
        """
        # 生成6位随机数字验证码
        code = ''.join(random.choices('0123456789', k=6))
        
        # 存储到Redis，设置过期时间
        key = f"{self.prefix}{email}"
        try:
            self.redis_client.set(key, code)
            self.redis_client.expire(key, self.expiry_seconds)
            logger.info(f"验证码已存储到Redis: {email} -> {code}, 过期时间: {self.expiry_seconds}秒")
        except redis.RedisError as e:
            logger.error(f"存储验证码到Redis失败: {str(e)}")
            raise
        
        return code
    
    def verify_code(self, email: str, code: str) -> bool:
        """
        验证用户提供的验证码是否正确
        
        Args:
            email: 用户邮箱
            code: 用户提供的验证码
            
        Returns:
            bool: 验证码是否正确
        """
        key = f"{self.prefix}{email}"
        try:
            stored_code = self.redis_client.get(key)
            
            if stored_code is None:
                logger.info(f"验证失败: 邮箱 {email} 的验证码不存在或已过期")
                return False
            
            # 验证码匹配，验证成功后删除该验证码
            if stored_code.decode('utf-8') == code:
                self.redis_client.delete(key)
                logger.info(f"验证成功: 邮箱 {email} 的验证码匹配")
                return True
            else:
                logger.info(f"验证失败: 邮箱 {email} 的验证码不匹配")
                return False
        except redis.RedisError as e:
            logger.error(f"验证验证码时Redis错误: {str(e)}")
            raise