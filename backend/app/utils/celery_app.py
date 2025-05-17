from celery import Celery
from config import current_config

def init_celery(app):
    """初始化 Celery 任务队列"""
    celery = Celery(
        app.import_name,
        broker=current_config.CELERY_BROKER_URL,
        backend=current_config.CELERY_RESULT_BACKEND
    )
    
    # 配置 Celery
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Shanghai',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=3600,  # 1小时
        worker_max_tasks_per_child=1000,
        worker_prefetch_multiplier=1
    )
    
    # 创建任务上下文
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    
    return celery 