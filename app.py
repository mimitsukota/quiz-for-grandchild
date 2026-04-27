import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import random

# --- 秘密の金庫（Secrets）からカギを取り出す ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("APIキーの設定が見つかりません。StreamlitのSecretsを設定してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- AIにクイズを作ってもらう関数 ---
def get_ai_quiz():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
    4歳の子供向けに、恐竜、妖怪、動物のどれかに関するクイズを1問作ってください。
    以下の形式（Pythonの辞書形式）だけで出力してください。余計な解説は不要です。
    {"genre": "ジャンル名", "q": "問題文（ガオー！など特徴を言う）", "a": "答え（ひらがな）", "img": "絵文字"}
    """
    response = model.generate_content(prompt)
    return eval(response.text)

# --- 画面の表示 ---
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = get_ai_quiz()

quiz = st.session_state.current_quiz

st.header(f"今回のジャンル： {quiz['genre']}")

if st.button("🔊 もんだいを きく"):
    tts = gTTS(quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.audio("q.mp3")

answer = st.text_input("こたえは なあに？（ひらがなでいれてね）")

if st.button("こたえあわせ"):
    if answer in quiz['a'] or quiz['a'] in answer:
        st.balloons()
        st.success(f"せいかい！ {quiz['a']} だよ！")
        st.write(f"## {quiz['img']}")
        if st.button("つぎのもんだいへ"):
            st.session_state.current_quiz = get_ai_quiz()
            st.rerun()
    else:
        st.error("おしい！もういちど かんがえてみてね。")
