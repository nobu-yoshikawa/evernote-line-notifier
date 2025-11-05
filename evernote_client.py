from datetime import datetime

def fetch_notes_by_dates(date_list):
    """
    本実装：Evernote APIで date_list の各日付のノートを取得して返す。
    返り値形式: list[dict] 例:
      [{"date": "2022-11-05", "title": "...", "content": "本文..."}]
    ----
    今はダミー（承認後にAPI実装へ差し替え）
    """
    notes = []
    for d in date_list:
        notes.append({
            "date": d.strftime("%Y-%m-%d"),
            "title": f"ダミーノート {d.strftime('%Y-%m-%d')}",
            "content": "ここにEvernote本文が入ります。（承認後に実データへ）"
        })
    return notes
