from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import current_config

def init_limiter(app):
    """初始化请求速率限制"""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=current_config.REDIS_URL
    )
    
    # 配置特定路由的限制
    limiter.limit("5 per minute")(app.blueprints.get('auth'))
    limiter.limit("10 per minute")(app.blueprints.get('api'))
    
    return limiter 