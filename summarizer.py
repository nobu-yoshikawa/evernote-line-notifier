import os

def summarize(text: str, max_chars: int = 600) -> str:
    """
    過去の日記を“単なる要約”ではなく、
    その日の朝に読み返すのに適した『学び・気づきの再定着型サマリー』として生成します。
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not text:
        return text[:max_chars]

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
あなたは内省コーチです。以下は過去の日記です。
この内容から「今日に活かせる学び・気づき・行動のヒント」を抽出し、
朝に自分自身へ送る“振り返りメッセージ”として日本語でまとめてください。

条件：
- 単なる要約ではなく、日記のエッセンスから「行動・考え方・気づき」に焦点を当てる
- 朝読むのに前向きになれるように、穏やかで希望のある語り口にする
- 最大500文字、見出し＋3つ以内の箇条書きで簡潔に
- 書き手は過去の自分、読み手は今日の自分という前提

【日記本文】
{text}
"""

        resp = model.generate_content(prompt)
        return resp.text.strip()[:max_chars]

    except Exception as e:
        return text[:max_chars]
