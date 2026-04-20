#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import schedule
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
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
# 你的API Key，在签到页面的已有密钥续期里的内容，替换成你自己的！
API_KEY = "sk-check...Z97K"
# 签到的时间，每天几点执行，比如 08:00 就是早上8点
CHECKIN_TIME = "08:00"
# -------------------------------------------------------------------

CHECKIN_URL = "https://gpt.qt.cool/checkin"

def do_checkin():
    """执行签到操作，自动识别表单地址，处理cookie"""
    logging.info("开始执行自动签到...")
    try:
        # 创建会话，自动处理cookie
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }
        
        # 1. 先访问签到页面，获取页面信息和cookie
        logging.info("访问签到页面，获取表单信息...")
        page_resp = session.get(CHECKIN_URL, headers=headers, timeout=15)
        page_resp.raise_for_status()
        
        # 2. 解析页面，自动找到表单的正确提交地址
        soup = BeautifulSoup(page_resp.text, 'html.parser')
        # 找到登录/签到的表单
        form = soup.find('form')
        if not form:
            raise Exception("未找到签到表单，请检查页面是否正常")
        # 拼接完整的提交地址
        action_url = urljoin(CHECKIN_URL, form.get('action', CHECKIN_URL))
        logging.info(f"找到表单提交地址：{action_url}")
        
        # 3. 提交表单，完成登录+签到
        logging.info("提交API Key，执行签到...")
        data = {
            "api_key": API_KEY
        }
        resp = session.post(action_url, headers=headers, data=data, timeout=15)
        resp.raise_for_status()
        
        # 4. 检查签到结果
        result_text = resp.text
        if "今日已签到" in result_text:
            logging.info("✅ 签到成功！今日已完成签到，成功领取余额奖励~")
        elif "已签到" in result_text:
            logging.info("ℹ️ 今日已经完成过签到了，无需重复操作。")
        else:
            logging.info(f"签到执行完成，页面返回：{result_text[:200]}")
        
    except Exception as e:
        logging.error(f"❌ 签到过程出错了：{str(e)}", exc_info=True)

def main():
    logging.info("自动签到服务已启动，将在每天 %s 自动执行签到..." % CHECKIN_TIME)
    # 设置定时任务
    schedule.every().day.at(CHECKIN_TIME).do(do_checkin)
    
    # 先执行一次测试
    do_checkin()
    
    # 循环等待
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
