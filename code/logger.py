# logger.py
"""
日志配置模块
提供统一的日志管理，支持不同级别的日志输出
"""

import logging
import sys
from datetime import datetime
import os

class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
        'RESET': '\033[0m'      # 重置
    }
    
    def format(self, record):
        # 添加颜色
        if hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_logger(name="KimiAutoMail", level=logging.INFO, log_to_file=True):
    """
    设置日志器
    
    Args:
        name (str): 日志器名称
        level (int): 日志级别 (DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50)
        log_to_file (bool): 是否同时输出到文件
    
    Returns:
        logging.Logger: 配置好的日志器
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # 创建格式化器
    console_formatter = ColoredFormatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（可选）
    if log_to_file:
        try:
            # 确保logs目录存在
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # 创建日志文件名（按日期）
            log_filename = f"kimi_auto_mail_{datetime.now().strftime('%Y%m%d')}.log"
            log_filepath = os.path.join(log_dir, log_filename)
            
            file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)  # 文件中记录所有级别的日志
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"无法创建日志文件: {e}")
    
    return logger

def get_logger(name="KimiAutoMail"):
    """
    获取日志器实例
    
    Args:
        name (str): 日志器名称
    
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(name)

# 预定义的日志级别配置
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,      # 开发调试：显示所有详细信息
    'INFO': logging.INFO,        # 用户模式：显示重要操作信息
    'WARNING': logging.WARNING,  # 警告模式：只显示警告和错误
    'ERROR': logging.ERROR,      # 错误模式：只显示错误信息
    'CRITICAL': logging.CRITICAL # 严重模式：只显示严重错误
}

def set_log_level(level_name):
    """
    动态设置日志级别
    
    Args:
        level_name (str): 日志级别名称 ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    level = LOG_LEVELS.get(level_name.upper(), logging.INFO)
    logger = get_logger()
    logger.setLevel(level)
    
    # 同时更新所有处理器的级别
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
            handler.setLevel(level)