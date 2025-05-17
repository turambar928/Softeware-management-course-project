from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest


def hash_password(password: str, method: str = 'pbkdf2:sha256', salt_length: int = 16) -> str:
    """
    对密码进行加密
    
    Args:
        password: 需要加密的密码
        method: 加密方法，默认为 pbkdf2:sha256
        salt_length: 盐值长度，默认为16
        
    Returns:
        str: 加密后的密码哈希值
        
    Raises:
        BadRequest: 当密码为空或无效时
    """
    if not password or not isinstance(password, str):
        raise BadRequest("密码不能为空且必须是字符串类型")
    
    try:
        return generate_password_hash(
            password,
            method=method,
            salt_length=salt_length
        )
    except Exception as e:
        raise BadRequest(f"密码加密失败: {str(e)}")


def verify_password(password: str, password_hash: str) -> bool:
    """
    验证密码是否匹配
    
    Args:
        password: 待验证的密码
        password_hash: 存储的密码哈希值
        
    Returns:
        bool: 密码是否匹配
        
    Raises:
        BadRequest: 当输入参数无效时
    """
    if not password or not password_hash:
        raise BadRequest("密码和密码哈希值不能为空")
        
    try:
        return check_password_hash(password_hash, password)
    except Exception as e:
        raise BadRequest(f"密码验证失败: {str(e)}")
