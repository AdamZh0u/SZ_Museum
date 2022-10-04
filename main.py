import time
import requests
import random
import json
from urllib.parse import quote
import time 
import sys
import warnings

import config

warnings.filterwarnings('ignore')

dates = config.get('dates')
token = config.get('token')
sku_id = config.get('sku_id')
user_ids = config.get('user_ids')

header_user_agent =  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307062c)'

## =================================================

request_header = {
    "Host": "api.cloud.sz-trip.com",
    "accept": "application/json, text/plain, */*",
    "origin": "https://m.cloud.sz-trip.com",
    "User-Agent": header_user_agent,
    "Referer": "https://m.cloud.sz-trip.com/VenueOrder",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "close"
}

request_api = "https://api.cloud.sz-trip.com/api/product/product_timestock_price?date=%s&sku_id=%s&token=%s"
order_api = 'https://api.cloud.sz-trip.com/api/order/create?data=%s&token=%s'

def wait_for_random_interval(is_show):
    interval_time = random.randint(7, 20)
    if is_show:
        print(f"等待随机时间间隔，防止服务器接口限流导致失败 : {interval_time} s")
    time.sleep(interval_time)

def search_tickets():   
    for date in dates:
        print(f'{date}搜索门票...')
        result_json = requests.get(request_api % (date, sku_id, token),
                                headers=request_header, timeout=15, verify=False).json()
        for i in result_json['data']:
            if i['stock_number'] >= 2:
                print(f"找到{i['stock_number']}张票")
                start_time = i['start_time']
                end_time = i['end_time']
                sale_date = i['sale_date']
                print(sale_date, start_time)
                return 1, (start_time, end_time, sale_date)
        print(f"无票")
    return 0,0    


def book_tickets(info):
    order_data = {"coupon_id": 0, 'source': "", "product_list": [{"type": "venue", "product_id": 4207, "sku_id": sku_id,
                                                                  "start_time": info[0], "end_time": info[1], "use_date": info[2], "visitors": user_ids, "product_num": 2, "remark": ""}]}
    try:
        res = requests.get(
            order_api % (quote(json.dumps(order_data)).replace('%20', ''),  token),
            headers=request_header, timeout=10, verify=False)
        if res.status_code == 200:
            return 1
    except:
        return 0

def main():
    i = 1
    while True:
        print('=='*30)
        print(f"...第{i}次尝试订票...")
        wait_for_random_interval(True)  
        have_tickets, info = search_tickets()

        if have_tickets == 1:
            print(f'开始订票, 日期{info[2]},入馆时间{info[0]}')
            success = book_tickets(info)
            if success == 1:
                print(f"\033[4;32m{i}已成功完成订票\033[0m")
            sys.exit(0)
        i += 1

if __name__ == '__main__':
    while True:
        time_now = time.strftime("%H:%M", time.localtime())
        print(time_now)
        if time_now == "08:00": # 8点开始运行
            print(f"【开始搜索 {dates} 门票 】")
            main()
        else:
            time.sleep(60)


