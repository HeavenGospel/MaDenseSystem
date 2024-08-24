import requests

url = 'http://localhost:3001/webhook/msg/v2?token=xvan'
headers = {'Content-Type': 'application/json'}
data = {'to': 'H小轩', 'data': {'content': '发现均线密集!'}}
def send_msg():
    try:
        response = requests.post(url, headers=headers, json=data)
    except requests.exceptions.RequestException as e:
        print("发送微信消息失败！")