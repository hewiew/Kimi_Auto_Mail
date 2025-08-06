# setup_kimi_login.py
# 首次登录Kimi的设置脚本

from playwright.sync_api import sync_playwright
import config

def setup_kimi_login():
    """
    打开浏览器，让用户手动登录Kimi，保存登录状态以供后续自动化使用。
    """
    with sync_playwright() as p:
        print("正在启动浏览器进行Kimi登录设置...")
        print("请在浏览器中手动登录您的Kimi账户。")
        
        try:
            # 启动持久化浏览器上下文（不使用无头模式，让用户可以看到浏览器）
            browser = p.chromium.launch_persistent_context(
                user_data_dir=config.USER_DATA_DIR,
                headless=False,  # 显示浏览器窗口
                args=['--no-sandbox']
            )
            
            page = browser.new_page()
            print("正在导航到Kimi网站...")
            page.goto("https://kimi.moonshot.cn/")
            
            print("\n" + "="*60)
            print("请在浏览器窗口中完成以下操作：")
            print("1. 登录您的Kimi账户（扫码或密码登录）")
            print("2. 确认登录成功后，关闭浏览器窗口")
            print("3. 回到此终端，按回车键继续...")
            print("="*60 + "\n")
            
            # 等待用户手动登录并确认
            input("登录完成后，请按回车键继续...")
            
            # 验证登录状态
            print("正在验证登录状态...")
            try:
                # 检查是否有输入框（登录成功的标志）
                page.wait_for_selector('textarea[placeholder*="输入"], textarea[placeholder*="问"]', timeout=10000)
                print("✅ 登录状态验证成功！")
                print("✅ 登录信息已保存，后续程序将自动使用此登录状态。")
            except:
                print("⚠️  无法验证登录状态，可能需要重新登录。")
                print("   请确保您已正确登录Kimi账户。")
            
            browser.close()
            
        except Exception as e:
            print(f"设置登录时发生错误: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Kimi登录设置工具")
    print("此脚本将帮助您设置Kimi的登录状态，以便后续自动化使用。")
    print()
    
    success = setup_kimi_login()
    
    if success:
        print("\n✅ 设置完成！")
        print("现在您可以运行 'python main.py' 来测试自动化工具了。")
    else:
        print("\n❌ 设置失败，请检查网络连接和Kimi网站状态。")