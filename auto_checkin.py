#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import schedule
from playwright.sync_api import sync_playwright
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('checkin.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# -------------------------- 请修改这里的配置 --------------------------
# 你的API Key，在签到页面的已有密钥续期里的那个输入框里的内容，比如 sk-xxxxxx
API_KEY = "sk-check...Z97K"  # 请替换成你自己的API Key！！！
# 签到的时间，每天几点执行，比如 08:00 就是早上8点
CHECKIN_TIME = "08:00"
# -------------------------------------------------------------------

CHECKIN_URL = "https://gpt.qt.cool/checkin"

def do_checkin():
    """执行签到操作"""
    logging.info("开始执行自动签到...")
    try:
        with sync_playwright() as p:
            # 启动无头浏览器，不会弹出窗口
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # 打开签到页面
            page.goto(CHECKIN_URL)
            logging.info("页面加载完成，准备输入API Key...")
            
            # 等待输入框加载
            api_input = page.wait_for_selector('input[placeholder="输入你的 API Key (sk-...)"]')
            # 清空输入框，输入API Key
            api_input.fill(API_KEY)
            logging.info("API Key已输入，点击登录/签到按钮...")
            
            # 点击登录按钮，这个按钮同时也是签到按钮
            login_btn = page.wait_for_selector('button:has-text("登录")')
            login_btn.click()
            
            # 等待页面响应，看看结果
            time.sleep(3)
            # 检查是否签到成功
            if page.locator(':has-text("今日已签到")').is_visible():
                logging.info("签到成功！今日已完成签到，获取了余额奖励~")
            else:
                # 看看有没有其他提示，比如已经签到过了
                if page.locator(':has-text("已签到")').is_visible():
                    logging.info("今日已经完成过签到了，无需重复操作。")
                else:
                    # 截图保存错误页面，方便排查
                    page.screenshot(path="checkin_error.png")
                    logging.warning("签到结果未知，已保存错误截图，请查看。")
            
            browser.close()
    except Exception as e:
        logging.error(f"签到过程出错了：{str(e)}", exc_info=True)

def main():
    logging.info("自动签到服务已启动，将在每天 %s 自动执行签到..." % CHECKIN_TIME)
    # 设置定时任务，每天指定时间执行签到
    schedule.every().day.at(CHECKIN_TIME).do(do_checkin)
    
    # 先执行一次签到，测试一下
    do_checkin()
    
    # 循环等待任务
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次任务

if __name__ == "__main__":
    main()
