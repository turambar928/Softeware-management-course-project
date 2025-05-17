import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from prometheus_flask_exporter import PrometheusMetrics
from config import current_config

def init_monitoring(app):
    """初始化监控系统"""
    # 初始化 Sentry
    if current_config.SENTRY_DSN:
        sentry_sdk.init(
            dsn=current_config.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=current_config.FLASK_ENV
        )
    
    # 初始化 Prometheus 指标
    metrics = PrometheusMetrics(app)
    
    # 注册默认指标
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # 添加自定义指标
    metrics.register_default(
        metrics.counter(
            'by_path_counter', 'Request count by request paths',
            labels={'path': lambda: request.path}
        )
    )
    
    return metrics 