from flask_swagger_ui import get_swaggerui_blueprint
from config import current_config

def init_swagger(app):
    """初始化 Swagger API 文档"""
    SWAGGER_URL = '/api/docs'  # Swagger UI 的 URL
    API_URL = '/static/swagger.json'  # API 文档的 JSON 文件路径
    
    # 创建 Swagger UI 蓝图
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Deepfake 检测系统 API"
        }
    )
    
    # 注册蓝图
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    return swaggerui_blueprint 