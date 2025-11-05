import requests
import os

token = os.environ["LINE_CHANNEL_TOKEN"]
url = "https://notify-api.line.me/api/notify"

message = "GitHub ActionsからのLINE通知テストです！🎉"

headers = {"Authorization": f"Bearer {token}"}
data = {"message": message}

response = requests.post(url, headers=headers, data=data)
print(response.status_code, response.text)
