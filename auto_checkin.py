#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import schedule
import requests
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
    """执行签到操作，直接用接口请求，不需要浏览器"""
    logging.info("开始执行自动签到...")
    try:
        # 模拟表单提交，直接发送API Key完成登录+签到
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "api_key": API_KEY
        }
        response = requests.post(CHECKIN_URL, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        
        # 检查结果
        if "今日已签到" in response.text:
            logging.info("签到成功！今日已完成签到，成功领取余额奖励~")
        elif "已签到" in response.text:
            logging.info("今日已经完成过签到了，无需重复操作。")
        else:
            logging.info("签到执行完成，页面返回结果：%s" % response.text[:100])
        
    except Exception as e:
        logging.error(f"签到过程出错了：{str(e)}", exc_info=True)

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
