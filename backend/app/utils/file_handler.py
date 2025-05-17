import os
import uuid
from werkzeug.utils import secure_filename
from config import current_config

class FileHandler:
    """文件处理工具类"""
    
    @staticmethod
    def save_file(file, folder='uploads'):
        """
        保存上传的文件
        
        Args:
            file: 上传的文件对象
            folder: 保存的文件夹名称
            
        Returns:
            str: 保存后的文件路径
        """
        if not file:
            return None
            
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # 确保目录存在
        save_dir = os.path.join(current_config.UPLOAD_FOLDER, folder)
        os.makedirs(save_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(save_dir, unique_filename)
        file.save(file_path)
        
        return file_path
    
    @staticmethod
    def delete_file(file_path):
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_file_size(file_path):
        """
        获取文件大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            int: 文件大小（字节）
        """
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    @staticmethod
    def is_allowed_file(filename, allowed_extensions=None):
        """
        检查文件类型是否允许
        
        Args:
            filename: 文件名
            allowed_extensions: 允许的文件扩展名列表
            
        Returns:
            bool: 是否允许
        """
        if allowed_extensions is None:
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'}
            
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions 