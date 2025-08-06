# mailer.py

import yagmail
import smtplib
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

def send_email(subject, content):
    """
    发送邮件，支持多种SMTP配置。

    Args:
        subject (str): 邮件主题。
        content (str): 邮件内容 (可以是HTML格式)。
    """
    try:
        print("正在连接SMTP服务器并发送邮件...")
        
        # 优先使用标准库smtplib（更稳定）
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = config.EMAIL_SENDER
            msg['To'] = config.EMAIL_RECEIVER
            
            # 添加HTML内容
            html_part = MIMEText(content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 创建SSL上下文
            context = ssl.create_default_context()
            
            # 根据端口选择连接方式
            if config.EMAIL_PORT == 587:
                # STARTTLS
                print("使用STARTTLS连接...")
                server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
                server.starttls(context=context)
            elif config.EMAIL_PORT == 465:
                # SSL
                print("使用SSL连接...")
                server = smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORT, context=context)
            else:
                # 无加密
                print("使用无加密连接...")
                server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
            
            # 启用调试模式（可选）
            # server.set_debuglevel(1)
            
            print("正在登录邮箱...")
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            
            print("正在发送邮件...")
            server.send_message(msg)
            server.quit()
            print(f"✅ 邮件已成功发送至 {config.EMAIL_RECEIVER}")
            
        except Exception as smtp_error:
            print(f"标准库发送失败，尝试使用yagmail: {smtp_error}")
            
            # 备用方案：使用yagmail
            try:
                # 根据端口决定加密方式
                if config.EMAIL_PORT == 587:
                    # STARTTLS加密
                    yag = yagmail.SMTP(
                        user=config.EMAIL_SENDER,
                        password=config.EMAIL_PASSWORD,
                        host=config.EMAIL_HOST,
                        port=config.EMAIL_PORT,
                        smtp_starttls=True,
                        smtp_ssl=False
                    )
                elif config.EMAIL_PORT == 465:
                    # SSL加密
                    yag = yagmail.SMTP(
                        user=config.EMAIL_SENDER,
                        password=config.EMAIL_PASSWORD,
                        host=config.EMAIL_HOST,
                        port=config.EMAIL_PORT,
                        smtp_starttls=False,
                        smtp_ssl=True
                    )
                else:
                    # 其他端口，尝试无加密
                    yag = yagmail.SMTP(
                        user=config.EMAIL_SENDER,
                        password=config.EMAIL_PASSWORD,
                        host=config.EMAIL_HOST,
                        port=config.EMAIL_PORT,
                    )
                
                yag.send(
                    to=config.EMAIL_RECEIVER,
                    subject=subject,
                    contents=content
                )
                yag.close()
                print(f"✅ 邮件已成功发送至 {config.EMAIL_RECEIVER} (使用yagmail)")
                
            except Exception as yagmail_error:
                raise Exception(f"所有邮件发送方式都失败了。SMTP错误: {smtp_error}, yagmail错误: {yagmail_error}")
            
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        print("\n请检查以下配置：")
        print("1. config.py中的邮箱配置是否正确")
        print("2. 授权码/应用密码是否为最新且有效")
        print("3. SMTP服务器地址和端口是否正确")
        print("4. 网络连接是否正常")
        print("5. 邮箱SMTP服务是否已开启")
        print("6. 防火墙是否阻止了SMTP连接")
        
        # 提供具体的调试信息
        print(f"\n当前配置：")
        print(f"SMTP服务器: {config.EMAIL_HOST}:{config.EMAIL_PORT}")
        print(f"发件邮箱: {config.EMAIL_SENDER}")
        print(f"收件邮箱: {config.EMAIL_RECEIVER}")
        print(f"授权码长度: {len(config.EMAIL_PASSWORD)} 字符")
        
        # 针对Outlook的特殊提示
        if "outlook.com" in config.EMAIL_HOST.lower():
            print("\n📧 Outlook邮箱特殊提示：")
            print("1. 确保已开启两步验证")
            print("2. 使用应用密码而非账户密码")
            print("3. 检查Microsoft账户安全设置")
            print("4. 尝试重新生成应用密码")

def test_email_config():
    """
    测试邮件配置是否正确
    """
    print("正在测试邮件配置...")
    test_subject = "Kimi邮件工具配置测试"
    test_content = """
    <html>
    <body>
        <h2>📧 邮件配置测试成功！</h2>
        <p>如果您收到这封邮件，说明邮件配置已正确设置。</p>
        <p>现在您可以正常使用Kimi自动邮件推送工具了。</p>
        <hr>
        <p><em>测试时间：{}</em></p>
    </body>
    </html>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    send_email(test_subject, test_content)

if __name__ == "__main__":
    # 如果直接运行此文件，则进行配置测试
    from datetime import datetime
    test_email_config()