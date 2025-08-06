# kimi_handler.py
"""
Kimi交互处理模块
负责与Kimi网站的所有交互操作
"""

import time
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError
import config
from logger import get_logger

logger = get_logger()

def check_chat_length(page):
    """
    检查当前对话的长度，判断是否需要创建新对话。
    
    Args:
        page: Playwright页面对象
        
    Returns:
        bool: True表示需要创建新对话，False表示可以继续使用当前对话
    """
    try:
        logger.debug("检查当前对话长度...")
        
        # 获取所有segment-container
        segment_containers = page.locator('.segment-container').all()
        segment_count = len(segment_containers)
        logger.debug(f"当前对话中有 {segment_count} 个segment-container")
        
        # 如果segment-container数量超过200（对话轮数超过100）
        if segment_count > 200:
            logger.warning(f"segment-container数量({segment_count})超过200，需要创建新对话")
            return True
        
        # 计算所有segment-container中的字符总量
        total_chars = 0
        for container in segment_containers:
            try:
                text = container.inner_text().strip()
                total_chars += len(text)
            except Exception as e:
                logger.debug(f"获取segment-container文本失败: {e}")
                continue
        
        logger.debug(f"当前对话字符总量: {total_chars}")
        
        # 如果字符总量超过10000
        if total_chars > 10000:
            logger.warning(f"字符总量({total_chars})超过10000，需要创建新对话")
            return True
        
        logger.info("对话长度在合理范围内，可以继续使用")
        return False
        
    except Exception as e:
        logger.error(f"检查对话长度时出错: {e}")
        # 出错时保守处理，继续使用当前对话
        return False


def rename_chat_title(page, new_title):
    """
    修改当前对话的标题。
    
    Args:
        page: Playwright页面对象
        new_title (str): 新的对话标题
        
    Returns:
        bool: 修改是否成功
    """
    try:
        logger.info(f"开始修改对话标题为: {new_title}")
        
        # 1. 找到当前对话（使用更新的选择器）
        current_chat_selectors = [
            '.router-link-active.router-link-exact-active.chat-info-item',
            '.router-link-active.chat-info-item',
            '.chat-info-item.router-link-active',
            '.history-part .chat-info-item.router-link-active',
            '.history-part .chat-info-item:first-child'
        ]
        
        current_chat = None
        for selector in current_chat_selectors:
            try:
                current_chat = page.locator(selector).first
                if current_chat.is_visible():
                    logger.debug(f"使用选择器找到当前对话: {selector}")
                    break
            except:
                continue
        
        if not current_chat or not current_chat.is_visible():
            logger.error("未找到当前对话元素")
            return False
        
        # 2. 鼠标悬停在对话上以显示more-btn
        logger.debug("鼠标悬停在对话上...")
        current_chat.hover()
        time.sleep(1)  # 等待more-btn显示
        
        # 3. 找到more-button并点击
        more_button_selectors = [
            '.more-btn',
            '.more-button', 
            '[data-testid*="more"]',
            'button[title*="更多"]',
            'button[aria-label*="更多"]'
        ]
        
        more_button = None
        for selector in more_button_selectors:
            try:
                more_button = current_chat.locator(selector).first
                if more_button.is_visible():
                    logger.debug(f"找到more-btn: {selector}")
                    break
            except:
                continue
        
        if not more_button or not more_button.is_visible():
            logger.error("未找到more-btn")
            return False
        
        more_button.click()
        logger.debug("已点击more-btn")
        time.sleep(1)
        
        # 3. 等待菜单展开，查找"编辑标题"选项
        edit_title_option = page.locator('text="编辑标题"').first
        edit_title_option.wait_for(timeout=3000)
        
        if not edit_title_option.is_visible():
            logger.error("未找到'编辑标题'选项")
            return False
        
        edit_title_option.click()
        logger.debug("已点击'编辑标题'选项")
        time.sleep(1)
        
        # 4. 在弹出的窗口中输入新标题
        # 查找输入框（可能是input或textarea）
        title_input = None
        input_selectors = [
            'input[type="text"]',
            'textarea',
            '[role="textbox"]',
            'input'
        ]
        
        for selector in input_selectors:
            try:
                title_input = page.locator(selector).last  # 使用last获取最新出现的输入框
                if title_input.is_visible():
                    break
            except:
                continue
        
        if not title_input or not title_input.is_visible():
            logger.error("未找到标题输入框")
            return False
        
        # 清空输入框并输入新标题
        title_input.click()
        title_input.press('Control+a')  # 使用快捷键全选
        title_input.fill(new_title)
        logger.debug(f"已输入新标题: {new_title}")
        time.sleep(0.5)
        
        # 5. 点击确定按钮
        confirm_selectors = [
            'button:has-text("确定")',
            'button:has-text("确认")',
            'button:has-text("保存")',
            '.confirm-button',
            '.save-button'
        ]
        
        confirm_clicked = False
        for selector in confirm_selectors:
            try:
                confirm_button = page.locator(selector).first
                if confirm_button.is_visible():
                    confirm_button.click()
                    logger.debug("已点击确定按钮")
                    confirm_clicked = True
                    break
            except:
                continue
        
        if not confirm_clicked:
            # 尝试按回车键确认
            try:
                title_input.press('Enter')
                logger.debug("已按回车键确认")
                confirm_clicked = True
            except:
                logger.error("无法确认标题修改")
                return False
        
        time.sleep(2)  # 等待标题更新
        logger.info("对话标题修改完成")
        return True
        
    except Exception as e:
        logger.error(f"修改对话标题时出错: {e}")
        return False


def get_kimi_response(prompt, use_existing_chat=True):
    """
    使用Playwright与Kimi网页版交互，获取回复。

    Args:
        prompt (str): 要发送给Kimi的提示词。
        use_existing_chat (bool): 是否使用现有对话，默认True

    Returns:
        str: Kimi的回复内容，如果失败则返回错误信息。
    """
    with sync_playwright() as p:
        logger.info("启动浏览器...")
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=config.USER_DATA_DIR,
                headless=True,
                args=['--no-sandbox']
            )
            page = browser.new_page()
            logger.info("导航到Kimi网站...")
            page.goto("https://kimi.moonshot.cn/", timeout=60000)

            # 等待页面加载
            logger.debug("等待页面加载...")
            page.wait_for_load_state('domcontentloaded', timeout=20000)
            page.wait_for_timeout(3000)
            logger.debug("页面加载完成")

            # 记录发送前的页面内容（用于后续差集去除历史信息）
            logger.debug("记录发送前的页面内容...")
            pre_send_content = ""
            try:
                pre_send_content = page.locator('body').inner_text()
                logger.debug(f"发送前页面内容长度: {len(pre_send_content)} 字符")
            except Exception as e:
                logger.debug(f"获取发送前内容失败: {e}")

            # 尝试使用现有对话或创建新对话
            chat_found = False
            need_new_chat = False  # 标记是否需要创建新对话
            
            if use_existing_chat:
                logger.info("尝试查找现有对话...")
                try:
                    # 使用多种选择器查找历史对话
                    chat_selectors = [
                        '.history-part .chat-info-item',
                        '.chat-info-item',
                        '.sidebar .chat-info-item',
                        '.sidebar li'
                    ]
                    
                    elements = []
                    for selector in chat_selectors:
                        try:
                            page.wait_for_selector(selector, timeout=2000)
                            elements = page.query_selector_all(selector)
                            if elements:
                                logger.debug(f"使用选择器 {selector} 找到 {len(elements)} 个历史对话")
                                break
                        except:
                            continue
                    
                    if not elements:
                        logger.warning("未找到任何历史对话")
                        raise Exception("未找到历史对话")

                    # 根据配置选择目标会话或使用第一个
                    target_element = None
                    if hasattr(config, 'TARGET_CHAT_NAME') and config.TARGET_CHAT_NAME:
                        for element in elements[:5]:  # 只检查前5个
                            try:
                                text = element.text_content().strip()
                                if config.TARGET_CHAT_NAME.lower() in text.lower():
                                    target_element = element
                                    logger.info(f"找到匹配的会话: '{text}'")
                                    break
                            except:
                                continue
                    
                    if not target_element and elements:
                        if not (hasattr(config, 'CREATE_NEW_IF_NOT_FOUND') and config.CREATE_NEW_IF_NOT_FOUND):
                            target_element = elements[0]
                            logger.debug("使用第一个可用会话")

                    if target_element:
                        target_element.click()
                        page.wait_for_timeout(2000)
                        chat_found = True
                        logger.info("成功选择现有对话")
                        
                        # 检查对话长度，判断是否需要创建新对话
                        if check_chat_length(page):
                            logger.warning("当前对话过长，将创建新对话")
                            need_new_chat = True
                            chat_found = False
                            
                except Exception as e:
                    logger.debug(f"查找现有对话失败: {e}")

            if not chat_found:
                logger.info("创建新对话...")
                # 修正新建对话按钮选择器
                new_chat_selectors = [
                    '.new-chat-btn',  # 实际的按钮类名
                    'button:has-text("新建会话")',  # 实际的按钮文字
                    'button:has-text("新建对话")',  # 备用文字
                    'button:has-text("新对话")',   # 备用文字
                    '.new-chat-button'  # 备用类名
                ]
                for selector in new_chat_selectors:
                    try:
                        btn = page.locator(selector).first
                        if btn.is_visible():
                            btn.click()
                            logger.debug(f"已点击新建会话按钮 (使用选择器: {selector})")
                            time.sleep(2)
                            need_new_chat = True  # 标记创建了新对话
                            break
                    except Exception as e:
                        logger.debug(f"选择器 {selector} 失败: {e}")
                        continue

            # 查找输入框
            logger.debug("查找输入框...")
            input_box = None
            try:
                input_box = page.locator('[role="textbox"]').first
                input_box.wait_for(timeout=5000)
                if not (input_box.is_visible() and input_box.is_enabled()):
                    raise Exception("输入框不可用")
                logger.debug("成功找到输入框")
            except Exception as e:
                logger.error(f"未找到可用的输入框: {e}")
                raise Exception("无法找到输入框，请检查Kimi网站是否正常或登录状态是否有效")

            # 输入提示词
            logger.debug("输入提示词...")
            actual_prompt = prompt
            if chat_found and hasattr(config, 'KIMI_CONTINUE_PROMPT') and config.KIMI_CONTINUE_PROMPT:
                actual_prompt = config.KIMI_CONTINUE_PROMPT
                logger.debug(f"使用继续对话提示词: {actual_prompt}")
            else:
                logger.debug(f"使用原始提示词: {actual_prompt[:50]}...")

            input_box.click()
            time.sleep(0.5)
            input_box.fill(actual_prompt)
            time.sleep(0.5)

            # 查找并点击发送按钮
            logger.debug("查找发送按钮...")
            send_button = None
            try:
                send_button = page.locator('.send-button').first
                send_button.wait_for(timeout=2000)
                if send_button.is_visible() and send_button.is_enabled():
                    # 记录点击前的初始SVG状态
                    logger.debug("记录发送按钮点击前的初始SVG状态...")
                    initial_svg_content = ""
                    try:
                        svg_element = send_button.locator('svg').first
                        if svg_element.is_visible():
                            initial_svg_content = svg_element.inner_html()
                            logger.debug(f"记录到初始SVG内容 (长度: {len(initial_svg_content)} 字符)")
                    except Exception as svg_e:
                        logger.debug(f"记录初始SVG失败: {svg_e}")
                    
                    # 点击发送按钮
                    send_button.click()
                    logger.debug("已点击发送按钮")
                    
                    # 等待Kimi回复生成完成 - 通过监测发送按钮SVG变化
                    logger.info("等待Kimi回复生成...")
                    
                    # 监测SVG变化，最长等待2分钟
                    generation_completed = False
                    max_wait_time = 300  # 最长等待5分钟
                    start_time = time.time()
                    check_interval = 1  # 每1秒检查一次，提高检测精度
                    
                    # 状态跟踪
                    is_generating = False  # 是否正在生成（SVG与初始状态不一致）
                    last_progress_time = 0  # 上次显示进度的时间
                    
                    logger.debug(f"开始监测发送按钮SVG变化，最长等待{max_wait_time}秒...")
                    logger.debug("监测逻辑：SVG变化 → 开始生成 → SVG恢复初始状态 → 生成完成")
                    
                    while time.time() - start_time < max_wait_time:
                        try:
                            current_svg_content = ""
                            svg_element = send_button.locator('svg').first
                            if svg_element.is_visible():
                                current_svg_content = svg_element.inner_html()
                            
                            # 检查当前SVG状态
                            if initial_svg_content:
                                svg_changed = current_svg_content != initial_svg_content
                                
                                if not is_generating and svg_changed:
                                    # SVG发生变化，开始生成
                                    is_generating = True
                                    elapsed_time = time.time() - start_time
                                    logger.info(f"检测到SVG变化，Kimi开始生成回复 (耗时: {elapsed_time:.1f}秒)")
                                
                                elif is_generating and not svg_changed:
                                    # SVG恢复初始状态，生成完成
                                    elapsed_time = time.time() - start_time
                                    logger.info(f"SVG恢复初始状态，Kimi回复生成完成 (总耗时: {elapsed_time:.1f}秒)")
                                    generation_completed = True
                                    break
                            
                            # 显示等待进度（每10秒显示一次）
                            elapsed = time.time() - start_time
                            if elapsed - last_progress_time >= 10:
                                status = "生成中..." if is_generating else "等待开始生成..."
                                logger.debug(f"等待中... ({elapsed:.0f}/{max_wait_time}秒) - {status}")
                                last_progress_time = elapsed
                            
                            time.sleep(check_interval)
                            
                        except Exception as monitor_e:
                            logger.debug(f"监测SVG时出错: {monitor_e}")
                            time.sleep(check_interval)
                            continue
                    
                    if not generation_completed:
                        if is_generating:
                            logger.warning(f"等待{max_wait_time}秒后SVG仍未恢复初始状态，可能Kimi仍在输出，继续尝试获取回复")
                        else:
                            logger.warning(f"等待{max_wait_time}秒后未检测到SVG变化，可能页面异常或生成很快，继续尝试获取回复")
                    
                    # 额外等待确保内容完全渲染
                    time.sleep(2)
                    
                else:
                    raise Exception("发送按钮不可用")
            except Exception as e:
                logger.warning(f"发送按钮点击失败，尝试按回车键: {e}")
                try:
                    input_box.press('Enter')
                    logger.debug("已按回车键发送")
                    # 如果使用回车键发送，等待固定时间
                    logger.debug("使用回车键发送，等待固定时间...")
                    time.sleep(20)
                except Exception as e2:
                    logger.error(f"按回车键也失败: {e2}")
                    raise Exception("无法发送消息，请检查页面状态")

            # 获取Kimi回复（使用segment_container类精确定位最新回复）
            logger.info("获取Kimi回复...")
            response_text = ""
            
            try:
                # 方案1：使用segment_container类获取最新回复
                logger.debug("尝试通过segment-container类获取最新回复...")
                
                # 首先尝试在chat-content-list容器中查找segment-container
                segment_containers = []
                try:
                    # 尝试在chat-content-list容器中查找
                    chat_content_list = page.locator('.chat-content-list').first
                    if chat_content_list.is_visible():
                        segment_containers = chat_content_list.locator('.segment-container').all()
                        logger.debug(f"在chat-content-list中找到 {len(segment_containers)} 个segment-container")
                    else:
                        # 如果没有chat-content-list，直接查找所有segment-container
                        segment_containers = page.locator('.segment-container').all()
                        logger.debug(f"直接查找到 {len(segment_containers)} 个segment-container")
                except Exception as e:
                    logger.debug(f"查找segment-container失败: {e}")
                    # 备用方案：直接查找所有segment-container
                    segment_containers = page.locator('.segment-container').all()
                    logger.debug(f"备用方案找到 {len(segment_containers)} 个segment-container")

                if segment_containers:
                    # 获取最后一个segment-container（最新的回复）
                    last_container = segment_containers[-1]
                    
                    # 尝试按paragraph类分段获取文本
                    logger.debug("尝试按paragraph类分段获取文本...")
                    paragraph_elements = last_container.locator('.paragraph').all()
                    
                    if paragraph_elements:
                        paragraph_texts = []
                        for para in paragraph_elements:
                            try:
                                para_text = para.inner_text().strip()
                                if para_text:
                                    paragraph_texts.append(para_text)
                            except Exception as para_e:
                                logger.debug(f"提取段落文本失败: {para_e}")
                                continue
                        
                        if paragraph_texts:
                            response_text = '\n\n'.join(paragraph_texts)
                            logger.debug(f"按paragraph类获取到 {len(paragraph_texts)} 个段落 (总长度: {len(response_text)} 字符)")
                        else:
                            logger.debug("未找到有效的paragraph内容，回退到整体提取...")
                            response_text = last_container.inner_text().strip()
                            logger.debug(f"整体提取获取到回复 (长度: {len(response_text)} 字符)")
                    else:
                        logger.debug("未找到paragraph类，使用整体提取...")
                        response_text = last_container.inner_text().strip()
                        logger.debug(f"从最后一个segment-container获取到回复 (长度: {len(response_text)} 字符)")
                    
                    # 检查是否包含用户输入（如果最后一个segment包含我们刚发送的内容，说明它可能是用户输入）
                    if actual_prompt[:20] in response_text:
                        logger.debug("最后一个segment-container包含用户输入，尝试倒数第二个...")
                        if len(segment_containers) >= 2:
                            second_last_container = segment_containers[-2]
                            
                            # 尝试从倒数第二个segment-container按paragraph类分段获取文本
                            logger.debug("尝试从倒数第二个segment-container按paragraph类分段获取文本...")
                            alt_paragraph_elements = second_last_container.locator('.paragraph').all()
                            
                            if alt_paragraph_elements:
                                alt_paragraph_texts = []
                                for para in alt_paragraph_elements:
                                    try:
                                        para_text = para.inner_text().strip()
                                        if para_text:
                                            alt_paragraph_texts.append(para_text)
                                    except Exception as para_e:
                                        logger.debug(f"提取倒数第二个段落文本失败: {para_e}")
                                        continue
                                
                                if alt_paragraph_texts:
                                    alt_response = '\n\n'.join(alt_paragraph_texts)
                                    response_text = alt_response
                                    logger.debug(f"从倒数第二个segment-container按paragraph类获取到 {len(alt_paragraph_texts)} 个段落 (总长度: {len(alt_response)} 字符)")
                                else:
                                    logger.debug("倒数第二个segment-container未找到有效的paragraph内容，回退到整体提取...")
                                    response_text = second_last_container.inner_text().strip()
                            else:
                                logger.debug("倒数第二个segment-container未找到paragraph类，使用整体提取...")
                                try:
                                    response_text = second_last_container.inner_text().strip()
                                except Exception as alt_e:
                                    logger.debug(f"从倒数第二个segment-container提取失败: {alt_e}")
                                    # 保持使用最后一个的结果
                                    pass
                            
                            if response_text:
                                logger.debug(f"从倒数第二个segment-container获取到回复 (长度: {len(response_text)} 字符)")
                    
            except Exception as e:
                logger.debug(f"从segment-container提取文本失败: {e}")
            
            if not response_text:
                logger.debug("未找到任何segment-container")

            # 如果segment-container方法失败，使用备用方案
            if not response_text:
                logger.debug("segment-container方法失败，使用备用方案...")
                
                # 备用方案1：查找对话区域的所有文本
                conversation_selectors = [
                    '.conversation-content',
                    '.chat-content',
                    '.message-list',
                    '.chat-messages',
                    '.conversation-list'
                ]
                
                for selector in conversation_selectors:
                    try:
                        conversation_area = page.locator(selector).first
                        if conversation_area.is_visible():
                            # 获取所有文本内容
                            full_content = conversation_area.inner_text()
                            
                            # 尝试通过差集去除发送前的内容
                            if pre_send_content and len(pre_send_content) > 100:
                                # 简单的差集处理：找到新增的内容
                                if len(full_content) > len(pre_send_content):
                                    # 获取新增的部分
                                    new_content = full_content[len(pre_send_content):].strip()
                                    if new_content:
                                        # 进一步清理：移除可能的用户输入
                                        lines = new_content.split('\n')
                                        collected_texts = []
                                        for line in lines:
                                            line = line.strip()
                                            if line and not line.startswith(actual_prompt[:20]):
                                                collected_texts.append(line)
                                        
                                        if collected_texts:
                                            response_text = '\n'.join(collected_texts)
                                            logger.debug(f"从对话区域获取到回复 (片段数: {len(collected_texts)}, 长度: {len(response_text)} 字符)")
                                            break
                    except Exception as e:
                        logger.debug(f"对话区域选择器 {selector} 失败: {e}")
                        continue
                
                # 备用方案2：获取页面后半部分的新内容
                if not response_text:
                    logger.debug("使用最终备用方案...")
                    try:
                        # 获取当前页面的所有文本
                        current_content = page.locator('body').inner_text()
                        
                        # 如果有发送前的内容记录，尝试找到差异
                        if pre_send_content and len(current_content) > len(pre_send_content):
                            # 简单的新内容提取
                            potential_new_content = current_content[len(pre_send_content):].strip()
                            if potential_new_content and len(potential_new_content) > 50:
                                response_text = potential_new_content
                                logger.debug(f"从页面后半部分获取回复 (长度: {len(response_text)} 字符)")
                        
                    except Exception as e:
                        logger.debug(f"最终备用方案失败: {e}")

            if not response_text:
                logger.error(f"获取回复时发生错误: {e}")
                response_text = "无法获取Kimi的回复内容，可能网站结构已更新或网络问题。"

            if response_text and len(response_text) > 50:
                logger.info(f"成功获取Kimi回复 (总长度: {len(response_text)} 字符)")
                preview = response_text[:100] + "..." if len(response_text) > 100 else response_text
                logger.debug(f"回复预览: {preview}")
            else:
                logger.error("未能获取到Kimi回复")
                response_text = "无法获取Kimi的回复内容，可能网站结构已更新或网络问题。"

            # 如果创建了新对话，尝试修改标题
            if need_new_chat and hasattr(config, 'TARGET_CHAT_NAME') and config.TARGET_CHAT_NAME:
                logger.info("检测到创建了新对话，开始修改对话标题...")
                title = config.TARGET_CHAT_NAME
                if rename_chat_title(page, title):
                    logger.info("对话标题修改成功")
                else:
                    logger.warning("对话标题修改失败，但不影响主要功能")

            # 关闭浏览器
            logger.debug("关闭浏览器...")
            browser.close()
            logger.debug("浏览器已关闭")

            return response_text.strip() if response_text else "无法获取Kimi的回复内容，可能网站结构已更新或网络问题。"

        except Exception as e:
            logger.error(f"与Kimi交互时发生错误: {e}")
            try:
                if 'browser' in locals() and browser:
                    browser.close()
                    logger.debug("浏览器已关闭")
            except Exception as close_error:
                logger.debug(f"关闭浏览器时出错: {close_error}")
            return f"自动化获取内容失败，错误信息: {e}"