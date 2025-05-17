import os
from app.init import create_app
from flask_cors import CORS
from config import current_config

app = create_app()

# 配置CORS
CORS(app, 
     origins=current_config.CORS_ORIGINS,
     supports_credentials=True,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not Found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal Server Error'}, 500

if __name__ == '__main__':
    # 确保上传目录存在
    os.makedirs(current_config.UPLOAD_FOLDER, exist_ok=True)
    
    # 启动应用
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=current_config.DEBUG,
        use_reloader=False
    )
