# main.py

import time
from datetime import datetime
import config
import mailer
from logger import setup_logger, LOG_LEVELS
from kimi_handler import get_kimi_response
from html_formatter import format_text_to_html, generate_email_html, generate_error_email_html

# 初始化日志器
logger = setup_logger(
    level=LOG_LEVELS.get(config.LOG_LEVEL.upper(), 20),  # 默认INFO级别
    log_to_file=getattr(config, 'LOG_TO_FILE', True)
)

def run(use_existing_chat=True):
    """
    主执行函数

    Args:
        use_existing_chat (bool): 是否使用现有对话，默认True
    """
    logger.info("开始执行Kimi每日邮件任务...")

    # 1. 从Kimi获取内容
    response = get_kimi_response(config.KIMI_PROMPT, use_existing_chat)

    if "失败" in response or "无法获取" in response:
        logger.error("获取Kimi内容失败，发送错误通知邮件")
        # 即使失败，也发送邮件通知用户
        today_str = datetime.now().strftime('%Y年%m月%d日')
        subject = f"Kimi邮件工具运行失败通知 {today_str}"
        error_content = generate_error_email_html(response)
        mailer.send_email(subject, error_content)
        return

    # 2. 发送邮件
    today_str = datetime.now().strftime('%Y年%m月%d日')
    subject = f"今日咨询推送 {today_str}"

    # 格式化内容
    formatted_content = format_text_to_html(response)
    html_content = generate_email_html(formatted_content)
    
    mailer.send_email(subject, html_content)
    logger.info("任务执行完毕")


if __name__ == "__main__":
    # 默认使用现有对话，如果需要新建对话可以传入False
    run(use_existing_chat=True)