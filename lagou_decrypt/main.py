# -*- coding: utf-8 -*-
from spider_main import spider_main
from tqdm import tqdm
import json
import time

category_list = ['电商平台', '汽车交易平台', '游戏', '工具类产品', '软件服务｜咨询', '数据服务｜咨询', 'IT技术服务｜咨询', '营销服务｜咨询', '人工智能服务', '物联网', '分类信息', '消费生活', '社交平台', '内容资讯', '内容社区', '社交媒体', '音频｜视频媒体', '短视频', 'MCN｜直播平台', '区块链', '信息安全', '信息检索', '新零售', '在线教育', '物流平台', '生活服务', '影视｜动漫', '新媒体', '科技金融', '居住服务', '新能源汽车制造', '智能硬件', '网络通信', '在线医疗', '旅游｜出行', '批发｜零售', '贸易｜进出口', '教育｜培训', '专业服务｜咨询', '物流｜运输', '文化传媒', '金融业', '房地产｜建筑｜物业', '制造业', '医疗｜保健｜美容', '服务业', '能源｜矿产｜环保', '农林牧渔', '休闲｜娱乐']

with open('data.jsonl', mode='w', encoding='utf-8') as f:
    for categorys in tqdm(category_list):
        if categorys == '在线医疗':
            min_range = 6
        else:
            min_range = 1

        for i in tqdm(range(min_range, 16)):
            original_data = {
                "city": "全国",   # 城市范围
                "pn": i,        # 页码
                "kd": categorys,    # 关键词
                "px": "new"      # 排序方式，new：最新，default：默认
            }

            data_json = spider_main(original_data)
            message = data_json.get('message', '')
            if message == '请求过于频繁':
                print(original_data)
                input(111111)
            else:
                save_dict = {"original_data": original_data, "data_json": data_json}
                f.write(json.dumps(save_dict, ensure_ascii=False) + "\n")
                time.sleep(5)

