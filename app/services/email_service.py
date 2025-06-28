import re
from typing import Dict, Any
from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models
from alibabacloud_tea_util import models as util_models
from config.settings import get_email_config


class EmailService:
    """邮件服务类，用于发送验证码邮件"""
    
    def __init__(self, 
                 access_key_id: str = None,
                 access_key_secret: str = None,
                 endpoint: str = None,
                 account_name: str = None,
                 template_path: str = None):
        """
        初始化邮件服务
        
        Args:
            access_key_id: 阿里云访问密钥ID
            access_key_secret: 阿里云访问密钥密码
            endpoint: 阿里云邮件服务端点
            account_name: 发件人邮箱账号
            template_path: 邮件模板路径
        """
        config = get_email_config()
        
        self.access_key_id = access_key_id or config['access_key_id']
        self.access_key_secret = access_key_secret or config['access_key_secret']
        self.endpoint = endpoint or config['endpoint']
        self.account_name = account_name or config['account_name']
        self.template_path = template_path or config['template_path']
        self.client = self._create_client()
        
    def _create_client(self) -> Dm20151123Client:
        """创建阿里云邮件服务客户端"""
        config = open_api_models.Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            endpoint=self.endpoint
        )
        return Dm20151123Client(config)
    
    def _load_template(self, code: str) -> str:
        """
        加载HTML模板并替换验证码
        
        Args:
            code: 验证码
            
        Returns:
            str: 替换验证码后的HTML内容
        
        Raises:
            IOError: 无法读取模板文件时抛出
        """
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return html_content.replace('{{code}}', code)
        except IOError as e:
            raise IOError(f"无法读取模板文件 - {str(e)}")
    
    def send_verification_email(self, 
                               to_address: str, 
                               code: str, 
                               subject: str = "验证码通知", 
                               from_alias: str = "家书万金") -> Dict[str, Any]:
        """
        发送验证码邮件
        
        Args:
            to_address: 收件人邮箱地址
            code: 6位数字验证码
            subject: 邮件主题，默认为"验证码通知"
            from_alias: 发件人别名，默认为"家书万金"
            
        Returns:
            Dict[str, Any]: 包含请求ID和状态的字典
            
        Raises:
            ValueError: 验证码格式不正确时抛出
            Exception: 发送邮件失败时抛出
        """
        # 验证验证码格式
        if not re.match(r'^\d{6}$', code):
            raise ValueError("验证码必须是6位数字")
        
        # 加载HTML模板并替换验证码
        html_body = self._load_template(code)
        
        # 构建请求
        request = dm_20151123_models.SingleSendMailRequest(
            account_name=self.account_name,
            address_type=1,
            reply_to_address=False,
            to_address=to_address,
            subject=subject,
            html_body=html_body,
            from_alias=from_alias
        )
        
        # 发送请求
        try:
            resp = self.client.single_send_mail_with_options(request, util_models.RuntimeOptions())
            return {"request_id": resp.body.request_id, "status": "success"}
        except Exception as error:
            error_msg = getattr(error, 'message', str(error))
            recommend_url = getattr(error, 'data', {}).get("Recommend", "")
            error_response = {"status": "error", "message": error_msg}
            if recommend_url:
                error_response["recommend"] = recommend_url
            raise Exception(error_response)