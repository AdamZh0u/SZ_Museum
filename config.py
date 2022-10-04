import os

# 以下参数根据自己的需要进行修改：
SYS_CONFIG = {
    # 用户token, 每天23点更新
    'token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    # 预约日期
    'dates': ['2022-10-04', '2022-10-05', '2022-10-06', '2022-10-07'],
    # 场馆标识
    'sku_id':1640,
    # 用户id
    'user_ids': "1298258,1298279"
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
