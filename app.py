import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import random
import json

# --- 秘密の金庫からカギを取り出す ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("APIキーの設定が見つかりません。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- AIにクイズを作ってもらう関数 ---
def get_ai_quiz():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
    4歳の子供向けに、恐竜、妖怪、動物のどれかに関するクイズを1問作ってください。
    以下のJSON形式だけで出力してください。
    {"genre": "ジャンル名", "q": "問題文", "a": "答えのひらがな", "img": "絵文字"}
    """
    response = model.generate_content(prompt)
    # 余計な装飾（```jsonなど）を削るお掃除
    txt = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(txt)

# --- アプリの動き ---
if 'current_quiz' not in st.session_state:
    with st.spinner('AIがクイズをかんがえ中...'):
        st.session_state.current_quiz = get_ai_quiz()

quiz = st.session_state.current_quiz

st.header(f"今回のジャンル： {quiz['genre']}")

if st.button("🔊 もんだいを きく"):
    tts = gTTS(quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.audio("q.mp3")

answer = st.text_input("こたえは なあに？")

if st.button("こたえあわせ"):
    if answer in quiz['a'] or quiz['a'] in answer:
        st.balloons()
        st.success(f"せいかい！ {quiz['a']} だよ！")
        st.write(f"## {quiz['img']}")
        if st.button("つぎのもんだいへ"):
            del st.session_state.current_quiz
            st.rerun()
    else:
        st.error("おしい！もういちど かんがえてみてね。")
