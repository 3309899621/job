import json
import parsel
from pymongo import MongoClient

client = MongoClient('mongodb://10.9.99.36:27017/')
db = client['lagou_db']
collection = db['jobs']

mydb = client['lagou_db']
mycol = mydb['jobs']
save_col = mydb['clear_data']

with open('data.jsonl', mode='w', encoding='utf-8') as f:
    for datas in mycol.find():
        category = datas['original_data']['kd']
        data_list = datas['data_json']['content']['positionResult']['result']
        try:
            for data in data_list:
                positionName = data['positionName']
                keywords = data['positionLables']
                content_html = data['positionDetail']
                response = parsel.Selector(content_html)
                content = ""
                for lines in response.xpath('//p/text()').extract():
                    if lines.strip():
                        content += "\n" + lines.strip()

                save_dict = {"positionName": positionName, "keywords": '/'.join(keywords).strip(), 'content': content}
                f.write(json.dumps(save_dict, ensure_ascii=False) + "\n")
                # save_col.insert_one(save_dict)
                # input(1111111)
        except Exception as e:
            print(e) 