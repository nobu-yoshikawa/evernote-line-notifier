import requests

# ↓↓↓ ここを実際のチャネルアクセストークンに置き換え（英数字のみ／前後に空白や改行を含めない）
LINE_CHANNEL_TOKEN = "sb5M1uCBcXkrmCw97TCCeO1M4psJveviPp0j+shKeVOxf1TweXIOYPnIi6l1VQd6cSsYk17eoBlO60+faMODi2pTST9xFCey9V4izENNMaoYADsSlGrHaxPui/PunfsYbeDmLFdcNESwbyfhz69T+gdB04t89/1O/w1cDnyilFU="

url = "https://api.line.me/v2/bot/message/broadcast"
headers = {
    "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}",
    "Content-Type": "application/json"
}
body = {
    "messages": [
        {"type": "text", "text": "テスト配信（Broadcast）"}  # 本文に日本語はOK（JSONはUTF-8）
    ]
}

r = requests.post(url, headers=headers, json=body, timeout=10)
print(r.status_code, r.text)
