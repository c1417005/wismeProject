from google import genai
from google.genai import types
from django.conf import settings


# モジュールレベルで Client を一度だけ生成して使い回す（施策3）。
# 毎回 new すると接続・初期化コストがかかるため。
_client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)


def GeminiAsk(Text = ""):
    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{Text} の意味を一言で説明してください。語数はなるべく少なく。辞書の説明のような簡潔で分かりやすい説明にしてください。",
        config=types.GenerateContentConfig(
            # 思考(thinking)をオフにして初回検索のレイテンシを削減（施策1）。
            # 一言定義の用途では思考は不要。
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            # 「一言」のはずが長文化すると生成に時間がかかるため上限を設定（施策4）。
            max_output_tokens=60,
        ),
    )
    return response.text
