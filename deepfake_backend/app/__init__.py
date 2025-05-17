from flask import Flask
from app.core.extensions import init_extensions
from app.utils.logger import setup_logger
from app.utils.monitoring import init_monitoring
from app.utils.swagger import init_swagger
from app.utils.celery_app import init_celery
from config import current_config

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(current_config)
    
    # 初始化扩展
    init_extensions(app)
    
    # 初始化日志
    setup_logger(app)
    
    # 初始化监控
    init_monitoring(app)
    
    # 初始化Swagger
    init_swagger(app)
    
    # 初始化Celery
    init_celery(app)
    
    # 注册蓝图
    from app.api.v1 import auth, user, deepfake
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(deepfake.bp)
    
    # 注册错误处理
    from app.core.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app 