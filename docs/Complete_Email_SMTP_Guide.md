# 完整邮箱SMTP配置指南

## 主流邮箱SMTP配置

### 1. QQ邮箱
**SMTP配置：**
- 服务器：`smtp.qq.com`
- 端口：`465`（SSL）或 `587`（STARTTLS）
- 加密：SSL/STARTTLS

**获取授权码步骤：**
1. 登录QQ邮箱网页版
2. 点击"设置" → "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"IMAP/SMTP服务"
5. 点击"生成授权码"
6. 通过短信验证后获得16位授权码
7. 在config.py中填入：
   ```python
   EMAIL_HOST = "smtp.qq.com"
   EMAIL_PORT = 465
   EMAIL_SENDER = "your_email@qq.com"
   EMAIL_PASSWORD = "your_16_digit_auth_code"
   ```

### 2. 163邮箱
**SMTP配置：**
- 服务器：`smtp.163.com`
- 端口：`465`（SSL）或 `25`（非加密）
- 加密：SSL

**获取授权码步骤：**
1. 登录163邮箱网页版
2. 点击"设置" → "POP3/SMTP/IMAP"
3. 开启"IMAP/SMTP服务"
4. 按照提示发送短信开启
5. 设置客户端授权密码（即授权码）
6. 在config.py中填入：
   ```python
   EMAIL_HOST = "smtp.163.com"
   EMAIL_PORT = 465
   EMAIL_SENDER = "your_email@163.com"
   EMAIL_PASSWORD = "your_auth_password"
   ```

### 3. Gmail邮箱
**SMTP配置：**
- 服务器：`smtp.gmail.com`
- 端口：`587`（STARTTLS）或 `465`（SSL）
- 加密：STARTTLS/SSL

**获取应用密码步骤：**
1. 登录Google账户：https://myaccount.google.com/
2. 左侧菜单选择"安全性"
3. 开启"两步验证"（如果还没开启）
4. 在"两步验证"下找到"应用密码"
5. 选择"邮件"和设备类型
6. 生成16位应用密码
7. 在config.py中填入：
   ```python
   EMAIL_HOST = "smtp.gmail.com"
   EMAIL_PORT = 587
   EMAIL_SENDER = "your_email@gmail.com"
   EMAIL_PASSWORD = "your_16_digit_app_password"
   ```

### 4. 126邮箱
**SMTP配置：**
- 服务器：`smtp.126.com`
- 端口：`465`（SSL）或 `25`（非加密）
- 加密：SSL

**获取授权码步骤：**
1. 登录126邮箱网页版
2. 点击"设置" → "POP3/SMTP/IMAP"
3. 开启"IMAP/SMTP服务"
4. 设置客户端授权密码
5. 在config.py中填入：
   ```python
   EMAIL_HOST = "smtp.126.com"
   EMAIL_PORT = 465
   EMAIL_SENDER = "your_email@126.com"
   EMAIL_PASSWORD = "your_auth_password"
   ```

## 重要注意事项

1. **安全性**：所有现代邮箱都不允许直接使用登录密码进行SMTP认证，必须使用专门的授权码/应用密码。

2. **两步验证**：Gmail要求先开启两步验证才能生成应用密码。

3. **端口选择**：
   - 465端口使用SSL加密
   - 587端口使用STARTTLS加密
   - 推荐使用587端口，兼容性更好

4. **测试方法**：配置完成后建议先手动运行一次程序测试邮件发送功能。

5. **授权码保存**：授权码只在生成时显示一次，请妥善保存。如果遗失，需要删除旧的重新生成。

## 常见问题排查

**发送失败常见原因：**
1. 授权码错误或过期
2. SMTP服务未开启
3. 网络防火墙阻止SMTP端口
4. 邮箱被临时限制（发送频率过高）

**解决方法：**
1. 重新生成授权码
2. 检查邮箱SMTP设置
3. 尝试不同的端口（465/587）
4. 降低发送频率，添加延时
