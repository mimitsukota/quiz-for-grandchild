import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json
import re

# --- 秘密の金庫からカギを取り出す ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("APIキーの設定（Secrets）をもう一度確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- AIにクイズを作ってもらう関数 ---
def get_ai_quiz():
    model = genai.GenerativeModel('gemini-1.5-flash')
    # AIへの命令をより厳しくしました
    prompt = "4歳の子供向けに、恐竜、妖怪、動物のクイズを1問作って。以下の形式のJSONデータだけを出力して。余計な挨拶は禁止。 {'genre': 'ジャンル', 'q': '問題文', 'a': '答え(ひらがな)', 'img': '絵文字'}"
    
    response = model.generate_content(prompt)
    
    # AIの返答からJSONの部分だけを無理やり抜き出す魔法
    match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if match:
        json_str = match.group()
        # シングルクォートをダブルクォートに変換
        json_str = json_str.replace("'", '"')
        return json.loads(json_str)
    else:
        # 万が一失敗した時の予備の問題
        return {"genre": "どうぶつ", "q": "おはなが ながーいのだーれだ？", "a": "ぞう", "img": "🐘"}

# --- アプリの表示 ---
if 'current_quiz' not in st.session_state:
    with st.spinner('AIが クイズを かんがえ中...'):
        st.session_state.current_quiz = get_ai_quiz()

quiz = st.session_state.current_quiz

st.header(f"今回のジャンル： {quiz['genre']}")

# 音声読み上げ
if st.button("🔊 もんだいを きく"):
    tts = gTTS(quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.audio("q.mp3")

answer = st.text_input("こたえは なあに？（ひらがな）")

if st.button("こたえあわせ"):
    if answer in quiz['a'] or quiz['a'] in answer:
        st.balloons()
        st.success(f"せいかい！ {quiz['a']} だよ！ {quiz['img']}")
        if st.button("つぎのもんだいへ"):
            del st.session_state.current_quiz
            st.rerun()
    elif answer == "":
        st.warning("なにか かいてみてね！")
    else:
        st.error("おしい！もういちど かんがえてみてね。")
