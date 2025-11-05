# main.py
import os
import requests
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

from evernote_client import fetch_notes_by_dates
from summarizer import summarize

# JST固定（GitHub Actionsでも日本時間で動かす）
JST = timezone(timedelta(hours=9))

def build_target_dates(today=None):
    """対象日：1/3/7/21/30/45/60日前＋過去の今日（1〜15年前）"""
    if today is None:
        today = datetime.now(JST).date()

    offsets = [1, 3, 7, 21, 30, 45, 60]
    days = [today - timedelta(days=o) for o in offsets]

    # 「過去の今日」1〜15年分（うるう年は+1日で補正）
    for years in range(1, 16):
        try:
            days.append(today - relativedelta(years=years))
        except ValueError:
            days.append(today - relativedelta(years=years) + timedelta(days=1))

    # 重複排除＆降順（新しい順）
    return sorted(set(days), reverse=True)

def format_digest(notes):
    """LINE本文を生成（全体で ~5,000字制限を意識／summarizerで要点抽出）"""
    if not notes:
        return "本日の対象日に該当する日記は見つかりませんでした。"

    lines = ["🌅【Evernote 日記ダイジェスト｜今日に活かす気づき】"]
    for n in notes:
        head = f"📘 {n.get('date','')}  {n.get('title','(無題)')}"
        body = summarize(n.get("content", ""), max_chars=500)  # 学び・気づき型の要約
        lines += [head, body, ""]

    text = "\n".join(lines)
    return text

def _split_for_line(text: str, limit: int = 4500):
    """LINEメッセージの安全マージン付き分割（1メッセージ ~5000字）"""
    chunks = []
    buf = text
    while buf:
        chunks.append(buf[:limit])
        buf = buf[limit:]
    return chunks or [""]

def send_broadcast(text: str):
    """
    Messaging API の Broadcast（全フォロワー配信）。
    フォロワーが自分だけなら実質“個人宛”。
    5件/リクエストの制約に合わせて分割送信。
    """
token = os.environ["LINE_CHANNEL_TOKEN"]  # GitHub Secrets のキー名と一致
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    chunks = _split_for_line(text)
    # 5メッセージ/リクエストの上限に合わせてバッチ化
    for i in range(0, len(chunks), 5):
        batch = chunks[i:i+5]
        body = {"messages": [{"type": "text", "text": c} for c in batch]}
        r = requests.post(url, headers=headers, json=body, timeout=20)
        print("Broadcast status:", r.status_code, r.text)
        r.raise_for_status()

def main():
    # 1) 対象日付を組む
    dates = build_target_dates()

    # 2) Evernoteから対象日のノートを取得（承認まではダミーが返る実装）
    notes = fetch_notes_by_dates(dates)

    # 3) 学び・気づき型の朝向けダイジェストに整形
    msg = format_digest(notes)

    # 4) Broadcastで配信（あなた1人が友だち＝実質個人宛）
    send_broadcast(msg)

if __name__ == "__main__":
    main()
