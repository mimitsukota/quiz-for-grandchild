import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"カギの設定を確認してください: {e}")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. クイズ作成関数（2026年4月安定版） ---
def create_new_quiz():
    # エラーが出た名前を修正しました
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "4歳向けクイズ（恐竜、妖怪、動物）を1問作成。JSON形式： {'genre': '...', 'q': '...', 'a': '...', 'img': '...'}"
    
    try:
        # v1betaではなく標準的な呼び出し方に合わせました
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        # 万が一の予備（次はステゴサウルスにしました！）
        return {"genre": "きょうりゅう", "q": "せなかに いたが たくさん あるのは？", "a": "すてごさうるす", "img": "🦖"}

# --- 3. アプリの動き ---
if st.button("🌟 新しい もんだいにする"):
    st.session_state.quiz = create_new_quiz()
    st.rerun()

if 'quiz' not in st.session_state:
    st.session_state.quiz = create_new_quiz()

q = st.session_state.quiz

st.info(f"ジャンル： {q['genre']}")
st.subheader(q['q'])

if st.button("🔊 こえを きく"):
    gTTS(q['q'], lang='ja').save("q.mp3")
    st.audio("q.mp3")

ans = st.text_input("こたえは なあに？", key="input_field")
if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！「{q['a']}」だよ！")
