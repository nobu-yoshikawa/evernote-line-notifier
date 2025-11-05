import os
import requests
import datetime

TOKEN = os.environ["LINE_CHANNEL_TOKEN"]  # ← GitHub Actions の Secret から受け取る

def send_broadcast(text: str):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    body = {"messages": [{"type": "text", "text": text}]}
    r = requests.post(url, headers=headers, json=body, timeout=10)
    r.raise_for_status()
    return r.status_code, r.text

if __name__ == "__main__":
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    msg = f"📒 本日のダイジェスト {today}\n自動送信テスト（06:28実行予定）"
    code, body = send_broadcast(msg)
    print(code, body)
