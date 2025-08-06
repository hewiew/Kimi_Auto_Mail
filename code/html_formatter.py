# html_formatter.py
"""
HTML格式化模块
负责将Kimi返回的文本转换为格式良好的HTML邮件内容
"""

import html
import re
from datetime import datetime
from logger import get_logger

logger = get_logger()

def format_text_to_html(text):
    """
    将Kimi返回的文本转换为格式良好的HTML
    
    Args:
        text (str): 原始文本内容
        
    Returns:
        str: 格式化后的HTML内容
    """
    if not text:
        return text
    
    logger.debug("开始格式化文本为HTML...")
    
    # 1. 先处理特殊字符转义
    text = html.escape(text)
    
    # 2. 将连续的换行符转换为段落分隔
    # 双换行符或更多 -> 段落分隔
    text = re.sub(r'\n\s*\n+', '\n\n', text)  # 标准化段落分隔
    
    # 3. 按段落分割
    paragraphs = text.split('\n\n')
    
    # 4. 处理每个段落 - 统一使用相同的格式
    formatted_paragraphs = []
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if not para:
            continue
            
        # 处理段落内的单个换行符（保留为<br>）
        para = para.replace('\n', '<br>')
        
        # 为了确保格式一致性，所有段落都使用相同的样式
        # 只有明确的特殊标记才使用不同样式
        if para.startswith('①') or para.startswith('②') or para.startswith('③') or para.startswith('④') or para.startswith('⑤'):
            # 问题项目（带圆框数字）
            formatted_paragraphs.append(f'<div class="qa-item">{para}</div>')
        elif para.startswith('•'):
            # 回答、金句、延伸项目（使用圆点标记）
            formatted_paragraphs.append(f'<div class="qa-item">{para}</div>')
        elif (para.endswith('：') or para.endswith(':')) and len(para) < 50:
            # 明确的标题（以冒号结尾且较短）
            formatted_paragraphs.append(f'<div class="section-title">{para}</div>')
        else:
            # 所有其他段落都使用统一的普通段落样式
            formatted_paragraphs.append(f'<p class="content-para">{para}</p>')
    
    result = '\n'.join(formatted_paragraphs)
    logger.debug(f"文本格式化完成，生成了 {len(formatted_paragraphs)} 个段落")
    return result

def generate_email_html(content, title="今日咨询推送"):
    """
    生成完整的邮件HTML内容
    
    Args:
        content (str): 已格式化的HTML内容
        title (str): 邮件标题
        
    Returns:
        str: 完整的HTML邮件内容
    """
    today_str = datetime.now().strftime('%Y年%m月%d日')
    
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ 
                font-family: 'Microsoft YaHei', Arial, sans-serif; 
                line-height: 1.8; 
                margin: 20px; 
                color: #333;
                background-color: #fafafa;
            }}
            .header {{ 
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: #2c3e50 !important;
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 25px;
                text-align: center;
                border: 2px solid #27ae60;
            }}
            .header h2 {{
                margin: 0 0 10px 0;
                font-size: 24px;
                color: #2c3e50 !important;
                font-weight: bold;
            }}
            .header p {{
                margin: 0;
                opacity: 1;
                color: #34495e !important;
                font-weight: 500;
            }}
            .content {{ 
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .content-para {{
                margin: 0 0 15px 0;
                text-align: justify;
            }}
            .qa-item {{
                margin: 20px 0;
                padding: 15px;
                background-color: #f8f9ff;
                border-left: 4px solid #667eea;
                border-radius: 5px;
            }}
            .section-title {{
                margin: 25px 0 15px 0;
                font-weight: bold;
                color: #444;
                font-size: 16px;
            }}
            .footer {{ 
                margin-top: 20px; 
                font-size: 12px; 
                color: #888;
                text-align: center;
                padding: 15px;
                background: white;
                border-radius: 10px;
            }}
            .footer hr {{
                border: none;
                height: 1px;
                background: linear-gradient(to right, transparent, #ddd, transparent);
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>🌟 {title}</h2>
            <p>日期：{today_str} | 来源：Kimi AI</p>
        </div>
        <div class="content">{content}</div>
        <div class="footer">
            <hr>
            <p>本邮件由Kimi自动邮件推送工具生成</p>
        </div>
    </body>
    </html>
    """
    
    logger.debug("生成完整邮件HTML内容")
    return html_content

def generate_error_email_html(error_message):
    """
    生成错误通知邮件的HTML内容
    
    Args:
        error_message (str): 错误信息
        
    Returns:
        str: 错误通知邮件的HTML内容
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    error_html = f"""
    <html>
    <body>
        <h2>Kimi自动邮件工具运行失败</h2>
        <p><strong>时间：</strong>{current_time}</p>
        <p><strong>错误详情：</strong></p>
        <pre>{error_message}</pre>
        <hr>
        <p><em>请检查：</em></p>
        <ul>
            <li>网络连接是否正常</li>
            <li>Kimi网站是否可以访问</li>
            <li>登录状态是否有效（可能需要重新运行 setup_kimi_login.py）</li>
        </ul>
    </body>
    </html>
    """
    
    logger.debug("生成错误通知邮件HTML内容")
    return error_html