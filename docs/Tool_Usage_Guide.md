# Kimi自动邮件推送工具 - 完整使用指南

## 🚀 工具启动方法

### 第一次使用（完整流程）

#### 步骤1：下载和解压
1. 下载 `Kimi_Auto_Mail` 文件夹到您的电脑
2. 解压到任意位置（如：`D:\Kimi_Auto_Mail`）

#### 步骤2：运行一键安装
**Windows用户：**
```cmd
# 右键点击 install.bat，选择"以管理员身份运行"
# 或者在命令提示符中：
cd D:\Kimi_Auto_Mail
install.bat
```

**Linux/macOS用户：**
```bash
cd /path/to/Kimi_Auto_Mail
chmod +x install.sh
./install.sh
```

安装过程会：
- 创建Python虚拟环境（在venv文件夹）
- 安装所有必需的Python库
- 下载Playwright浏览器内核
- 可能需要5-10分钟，请耐心等待

#### 步骤3：配置邮箱信息
1. 进入 `code` 文件夹
2. 将 `config.py.template` 重命名为 `config.py`
3. 打开 `config.py` 文件，填入您的邮箱配置：
   ```python
   EMAIL_HOST = "smtp-mail.126.com"  # 您的SMTP服务器
   EMAIL_PORT = 465                      # SMTP端口
   EMAIL_SENDER = "your_email@126.com"    # 发件邮箱
   EMAIL_PASSWORD = "your_app_password"       # 应用密码（不是登录密码！）
   EMAIL_RECEIVER = "your_email@126.com"  # 收件邮箱
   ```

#### 步骤4：首次手动登录Kimi
这一步只需要做一次，用于保存登录状态：

**Windows：**
```cmd
cd Path\to\Your\Kimi_Auto_Mail
.\venv\Scripts\activate.bat
cd code
python setup_kimi_login.py
```

**Linux/macOS：**
```bash
cd /path/to/Kimi_Auto_Mail
source venv/bin/activate
cd code
python setup_kimi_login.py
```

会弹出浏览器窗口，您需要：
1. 在浏览器中登录Kimi（扫码或密码都可以）
2. 登录成功后关闭浏览器
3. 回到终端按回车键

#### 步骤5：测试运行
```cmd
# Windows
cd Path\to\Your\Kimi_Auto_Mail
.\venv\Scripts\activate.bat
cd code
python main.py

# Linux/macOS
cd /path/to/Kimi_Auto_Mail
source venv/bin/activate
cd code
python main.py
```

如果一切正常，您会看到：
- "正在启动Kimi自动邮件工具..."
- "正在访问Kimi..."
- "正在发送邮件..."
- "任务完成！邮件已发送。"

### 日常使用（设置定时任务后）

#### Windows定时任务设置
1. 打开"任务计划程序"
2. 点击"创建任务"
3. **常规**选项卡：
   - 名称：`Kimi Daily Email`
   - 选择"不管用户是否登录都要运行"
4. **触发器**选项卡：
   - 新建触发器
   - 开始任务：按计划时间
   - 设置：每天
   - 时间：选择您希望的时间（如8:00）
5. **操作**选项卡：
   - 新建操作
   - 程序或脚本：`Path\to\Your\Kimi_Auto_Mail\venv\Scripts\python.exe`
   - 添加参数：`main.py`
   - 起始于：`Path\to\Your\Kimi_Auto_Mail\code`

#### Linux/macOS定时任务设置（cron）
```bash
# 编辑crontab
crontab -e

# 添加以下行（每天8:00执行）
0 8 * * * /path/to/Kimi_Auto_Mail/venv/bin/python /path/to/Kimi_Auto_Mail/code/main.py >> /path/to/Kimi_Auto_Mail/cron.log 2>&1
```

### 💡 使用技巧

#### 手动运行（测试用）
```cmd
# Windows
cd Path\to\Your\Kimi_Auto_Mail
.\venv\Scripts\activate.bat
cd code
python main.py

# Linux/macOS
cd /path/to/Kimi_Auto_Mail
source venv/bin/activate
cd code
python main.py
```

#### 查看日志
- Windows：查看任务计划程序中的历史记录
- Linux/macOS：查看 `cron.log` 文件

#### 更新配置
如需修改邮件内容或时间：
1. 编辑 `config.py` 文件
2. 修改相应配置
3. 重新运行即可（无需重新安装）

#### 重新登录Kimi
如果Kimi登录过期：
1. 删除 `playwright_user_data` 文件夹
2. 重新执行步骤4的登录过程

## 🔧 故障排除

### 常见问题

**1. 邮件发送失败**
- 检查邮箱授权码是否正确
- 确认SMTP服务已开启
- 参考《完整邮箱SMTP配置指南》重新配置

**2. Kimi访问失败**
- 检查网络连接
- 重新登录Kimi
- 确认Kimi网站可正常访问

**3. 定时任务不运行**
- Windows：检查任务计划程序中的任务状态
- Linux/macOS：检查crontab设置和权限

**4. Python环境问题**
- 确保使用虚拟环境中的Python
- 重新运行安装脚本

### 获取帮助
如遇到其他问题，请检查：
1. 所有路径是否使用绝对路径
2. Python虚拟环境是否正确激活
3. 网络连接是否正常
4. 邮箱和Kimi账户是否正常

## 📁 文件结构说明

```
Kimi_Auto_Mail/
├── venv/                     # Python虚拟环境（安装后生成）
├── code/                     # 源代码目录
│   ├── main.py              # 主程序
│   ├── mailer.py            # 邮件发送模块
│   ├── config.py            # 配置文件（用户填写）
│   ├── setup_kimi_login.py  # Kimi登录设置脚本
│   ├── playwright_user_data/ # Kimi登录状态（首次登录后生成）
│   └── requirements.txt     # Python依赖列表
├── install.bat              # Windows安装脚本
├── install.sh               # Linux/macOS安装脚本
└── docs/                    # 说明文档
    ├── Tool_Usage_Guide.md      # 使用指南
    ├── Complete_Email_SMTP_Guide.md  # 邮箱配置指南
    └── Outlook_SMTP_Setup_Guide.md   # Outlook专用指南
```

## ⚠️ 重要提醒

1. **授权码安全**：请妥善保管邮箱授权码，不要泄露给他人
2. **定期检查**：建议每周检查一次邮件接收情况
3. **网络要求**：工具需要稳定的网络连接访问Kimi
4. **系统要求**：支持Windows 10+、macOS 10.14+、Ubuntu 18.04+
5. **Python版本**：需要Python 3.8或更高版本

祝您使用愉快！📧✨
