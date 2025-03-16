import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
import ssl
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
import websocket

answer = ""

class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    def create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        v = {"authorization": authorization, "date": date, "host": self.host}
        return self.Spark_url + '?' + urlencode(v)

def on_error(ws, error):
    print("### error:", error)

def on_close(ws, one, two):
    print(" ")

def on_open(ws):
    thread.start_new_thread(run, (ws,))

def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain=ws.domain, question=ws.question))
    ws.send(data)

def on_message(ws, message):
    global answer
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        content = choices["text"][0]["content"]
        answer += content
        if choices["status"] == 2:
            ws.close()

def gen_params(appid, domain, question):
    data = {
        "header": {"app_id": appid, "uid": "1234"},
        "parameter": {"chat": {"domain": domain, "random_threshold": 0.5, "max_tokens": 2048, "auditing": "default"}},
        "payload": {"message": {"text": question}}
    }
    return data

def get_spark_response(question, appid="3549e948", api_key="65da35f93650aded57ee03e8668752ff",
                      api_secret="OTg2ZjA1NTJhMzI4ZTVjZmNiMWQwN2I0", spark_url="wss://spark-api.xf-yun.com/v1.1/chat",
                      domain="lite"):
    global answer
    answer = ""
    ws_param = Ws_Param(appid, api_key, api_secret, spark_url)
    ws_url = ws_param.create_url()
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question  # 传入完整的对话历史
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return answer

# 辅助函数：计算对话历史的总长度
def get_length(history):
    return sum(len(item["content"]) for item in history)

# 辅助函数：限制对话历史的长度
def trim_history(history, max_length=8000):
    while get_length(history) > max_length and len(history) > 1:
        history.pop(0)  # 删除最早的记录
    return history