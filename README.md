# 🤖 Kimi自动邮件推送工具

一个**完全免费**的自动化工具，每天定时从Kimi AI获取信息并通过邮件推送给您。

## ✨ 核心特性

- 🆓 **完全免费** - 无需API费用，使用网页自动化技术
- 📧 **邮件推送** - 支持所有主流邮箱（QQ、163、Gmail、Outlook等）
- ⏰ **定时运行** - 支持Windows/Linux/macOS定时任务
- 🔐 **一次登录** - 首次手动登录Kimi后，永久保存登录状态
- 🎯 **智能内容** - 基于"信息破茧助手"prompt，每日推送5个精选话题
- 📱 **本地部署** - 数据安全，完全在您的设备上运行

## 🚀 快速开始

### 1. 下载项目
下载并解压 `Kimi_Auto_Mail` 文件夹到任意位置

### 2. 一键安装
**Windows:**
```cmd
双击运行 install.bat
```

**Linux/macOS:**
```bash
./install.sh
```

### 3. 配置邮箱
1. 将 `code/config.py.template` 重命名为 `code/config.py`
2. 填入您的邮箱配置（详见配置指南）

### 4. 首次登录
```bash
# 激活虚拟环境后运行(如何激活环境可以查看Tool_Usage_Guide.md)
python code/setup_kimi_login.py
```

### 5. 测试运行
```bash
# 激活虚拟环境后运行(如何激活环境可以查看Tool_Usage_Guide.md)
python code/main.py
```

### 6. 设置定时任务
- **Windows**: 使用任务计划程序
- **Linux/macOS**: 使用cron

## 📁 项目结构

```
Kimi_Auto_Mail/
├── venv/                     # Python虚拟环境
├── code/                     # 源代码
│   ├── main.py              # 主程序
│   ├── mailer.py            # 邮件模块
│   ├── config.py            # 配置文件（用户填写）
│   ├── setup_kimi_login.py  # 登录设置脚本
│   └── requirements.txt     # 依赖列表
├── docs/                     # 详细文档
│   ├── Tool_Usage_Guide.md           # 完整使用指南
│   ├── Complete_Email_SMTP_Guide.md  # 邮箱配置指南
│   └── Outlook_SMTP_Setup_Guide.md   # Outlook专用指南
├── install.bat              # Windows安装脚本
└── install.sh               # Linux/macOS安装脚本
```

## 📧 支持的邮箱（发件邮箱）

| 邮箱类型 | SMTP服务器 | 端口 | 获取授权码方法 |
|---------|-----------|------|---------------|
| QQ邮箱 | smtp.qq.com | 465 | 邮箱设置→账户→开启SMTP→生成授权码 |
| 163邮箱 | smtp.163.com | 465 | 邮箱设置→POP3/SMTP→开启→设置授权密码 |
| Gmail | smtp.gmail.com | 587 | Google账户→安全性→两步验证→应用密码 |
| 126邮箱 | smtp.126.com | 587 | 邮箱设置→POP3/SMTP→开启→设置授权密码 |

## 🔧 核心技术

- **网页自动化**: Playwright
- **邮件发送**: yagmail + smtplib (双重保障)
- **定时任务**: 操作系统级定时任务
- **登录保持**: 持久化浏览器上下文

## 📋 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8或更高版本
- **网络**: 稳定的互联网连接
- **存储**: 约200MB空间（包括浏览器内核）

## 📖 详细文档

- [完整使用指南](docs/Tool_Usage_Guide.md) - 详细的安装和使用说明
- [邮箱配置指南](docs/Complete_Email_SMTP_Guide.md) - 各种邮箱的SMTP配置方法
- [Outlook配置指南](docs/Outlook_SMTP_Setup_Guide.md) - Outlook邮箱专用指南

## 🛡️ 安全说明

- **本地运行**: 所有数据处理在您的设备上进行
- **登录安全**: 使用Playwright安全保存登录状态
- **授权码**: 邮箱授权码仅保存在本地配置文件中
- **开源透明**: 所有代码可查看和审计

## ❓ 常见问题

**Q: 为什么不使用Kimi API？**
A: API需要付费，我们提供完全免费的网页自动化方案。

**Q: 登录状态会过期吗？**
A: 通常很久才过期，如果过期可以重新运行登录设置脚本。

**Q: 支持自定义prompt吗？**
A: 支持，在config.py中修改KIMI_PROMPT即可。

**Q: 可以修改发送时间吗？**
A: 可以，通过修改定时任务配置调整发送时间。

## 🔄 更新日志

### v1.0.0
- ✅ 首次发布
- ✅ 支持Kimi网页自动化
- ✅ 支持主流邮箱SMTP
- ✅ 跨平台定时任务支持
- ✅ 完整的文档和指南

## 📞 技术支持

如遇到问题，请检查：
1. 网络连接是否正常
2. 邮箱配置是否正确
3. Kimi登录状态是否有效
4. 系统时间是否正确

---

**免责声明**: 本工具仅供学习和个人使用，请遵守相关网站的使用条款。
