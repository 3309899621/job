import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")

import time
import json
import execjs
import requests
from lxml import etree
from urllib import parse

aes_key = ""
secret_key_value = ""

with open('lagou.js', 'r', encoding='utf-8') as f:
    lagou_js = execjs.compile(f.read())

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

x_anit = {
    "x-anit-forge-code": "0",
    "x-anit-forge-token": None
}

global_cookies = {
    "login": "true",
    "gate_login_token": "",
    "_putrc": "02EF55A3833232D8123F89F2B170EADC",
    "JSESSIONID": "ABAABJAABBGACAEF1408EBFC6D0FAE5FBDE3CAC7F4A92C8"
}

def get_user_trace_token() -> str:
    json_url = "https://a.lagou.com/json"
    headers = {
        "Host": "a.lagou.com",
        "Referer": "https://www.lagou.com/",
        "User-Agent": UA
    }
    params = {
        "lt": "trackshow",
        "t": "ad",
        "v": 0,
        "dl": "https://www.lagou.com/",
        "dr": "https://www.lagou.com",
        "time": str(int(time.time() * 1000))
    }
    response = requests.get(url=json_url, headers=headers, params=params)
    user_trace_token = response.cookies.get_dict()["user_trace_token"]
    return user_trace_token


def get_lg_stoken(original_data: dict) -> str:
    token_url = "https://www.lagou.com/wn/jobs"
    token_headers = {
        "Host": "www.lagou.com",
        "Referer": "https://www.lagou.com/",
        "User-Agent": UA
    }
    params = {
        "kd": original_data["kd"],
        "city": original_data["city"]
    }
    token_response = requests.get(url=token_url, params=params, headers=token_headers, cookies=global_cookies, allow_redirects=False)
    if token_response.status_code != 302:
        raise Exception("获取跳转链接异常！检查 global_cookies 是否已包含 __lg_stoken__！")
    security_check_url = token_response.headers["Location"]
    if "login" in security_check_url:
        raise Exception("IP 被关进小黑屋啦！需要登录！请补全登录后的 Cookie，或者自行添加代理！")
    parse_result = parse.urlparse(security_check_url)
    security_check_params = parse_result.query
    security_check_js_name = parse.parse_qs(security_check_params)["name"][0]

    js_url = "https://www.lagou.com/common-sec/dist/" + security_check_js_name + ".js"
    js_headers = {
        "Host": "www.lagou.com",
        "Referer": security_check_url,
        "User-Agent": UA
    }
    js_response = requests.get(url=js_url, headers=js_headers, cookies=global_cookies).text
    lg_js = """
    window = {
        "location": {
            "hostname": "www.lagou.com",
            "search": '?%s'
        }
    }
    function getLgStoken(){
        return window.gt.prototype.a()
    }
    """ % security_check_params + js_response

    lg_stoken = execjs.compile(lg_js).call("getLgStoken")
    return lg_stoken


def update_cookies(original_data: dict) -> None:
    global global_cookies
    user_trace_token = get_user_trace_token()
    x_http_token = lagou_js.call("getXHttpToken", "user_trace_token=" + user_trace_token)
    global_cookies.update({
        "user_trace_token": user_trace_token,
        "X_HTTP_TOKEN": x_http_token
    })

    # 获取 __lg_stoken__
    lg_stoken = get_lg_stoken(original_data)
    global_cookies.update({
        "__lg_stoken__": lg_stoken,
    })


def update_aes_key() -> None:
    global aes_key, secret_key_value
    url = "https://gate.lagou.com/system/agreement"
    headers = {
        "Content-Type": "application/json",
        "Host": "gate.lagou.com",
        "Origin": "https://www.lagou.com",
        "Referer": "https://www.lagou.com/",
        "User-Agent": UA
    }
    encrypt_data = lagou_js.call("getAesKeyAndRsaEncryptData")
    aes_key = encrypt_data["aesKey"]
    rsa_encrypt_data = encrypt_data["rsaEncryptData"]
    data = {"secretKeyDecode": rsa_encrypt_data}
    response = requests.post(url=url, headers=headers, json=data).json()
    secret_key_value = response["content"]["secretKeyValue"]


def update_x_anit(original_data: dict) -> None:
    url = "https://www.lagou.com/wn/jobs"
    headers = {
        "Host": "www.lagou.com",
        "Referer": "https://www.lagou.com/",
        "User-Agent": UA
    }
    params = {
        "kd": original_data["kd"],
        "city": original_data["city"]
    }
    response = requests.get(url=url, params=params, headers=headers, cookies=global_cookies)
    tree = etree.HTML(response.text)
    next_data_json = json.loads(tree.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
    submit_code = next_data_json["props"]["tokenData"]["submitCode"]
    submit_token = next_data_json["props"]["tokenData"]["submitToken"]
    if not submit_code or not submit_token:
        raise Exception("submitCode & submitToken 为空，请检查 JSESSIONID 是否正确！")
    global x_anit
    x_anit["x-anit-forge-code"] = submit_code
    x_anit["x-anit-forge-token"] = submit_token


def get_header_params(original_data: dict) -> dict:
    u = "https://www.lagou.com/jobs/v2/positionAjax.json"
    return {
        "traceparent": lagou_js.call("getTraceparent"),
        "X-K-HEADER": secret_key_value,
        "X-S-HEADER": lagou_js.call("getXSHeader", aes_key, original_data, u),
        "X-SS-REQ-HEADER": json.dumps({"secret": secret_key_value})
    }


def get_encrypted_data(original_data: dict) -> str:
    encrypted_data = lagou_js.call("getRequestData", aes_key, original_data)
    return encrypted_data


def get_data(original_data: dict, encrypted_data: str, header_params: dict) -> dict:
    url = "https://www.lagou.com/jobs/v2/positionAjax.json"
    referer = parse.urljoin("https://www.lagou.com/wn/jobs?", parse.urlencode(original_data))
    headers = {
        # "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.lagou.com",
        "Origin": "https://www.lagou.com",
        "Referer": referer,
        "traceparent": header_params["traceparent"],
        "User-Agent": UA,
        "X-K-HEADER": header_params["X-K-HEADER"],
        "X-S-HEADER": header_params["X-S-HEADER"],
        "X-SS-REQ-HEADER": header_params["X-SS-REQ-HEADER"],
    }
    headers.update(x_anit)

    data = {"data": encrypted_data}
    response = requests.post(url=url, headers=headers, cookies=global_cookies, data=data).json()
    if "status" in response:
        if not response["status"] and "操作太频繁" in response["msg"]:
            raise Exception("获取数据失败！msg：%s！可以尝试补全登录后的 Cookies，或者添加代理！" % response["msg"])
        else:
            raise Exception("获取数据异常！请检查数据是否完整！")
    else:
        response_data = response["data"]
        decrypted_data = lagou_js.call("getResponseData", response_data, aes_key)
        return decrypted_data

def spider_main(original_data):
    __lg_stoken__ = global_cookies.pop('__lg_stoken__', '')
    if '__lg_stoken__' not in global_cookies:
        need_init = True
        while need_init:
            update_cookies(original_data)
            update_aes_key()
            if "login" in global_cookies:
                update_x_anit(original_data)
            need_init = False

    header_params = get_header_params(original_data)
    encrypted_data = get_encrypted_data(original_data)
    data = get_data(original_data, encrypted_data, header_params)
    return data