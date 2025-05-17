from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def init_extensions(app):
    """初始化所有扩展"""
    # 初始化数据库
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 初始化JWT
    jwt.init_app(app)
    
    # 初始化CORS
    cors.init_app(app)
    
    # 初始化缓存
    cache.init_app(app)
    
    # 初始化限流器
    limiter.init_app(app)
    
    return app 