import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 診断開始 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"【診断】カギの設定が読み込めません: {e}")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def create_new_quiz():
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = "4歳向けクイズ（恐竜、妖怪、動物）を1問作成。JSON形式： {'genre': '...', 'q': '...', 'a': '...', 'img': '...'}"
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        # ここでエラーの正体を表示します！
        st.warning(f"AIが答えられませんでした（理由: {e}）。予備の問題を出します。")
        return {"genre": "きょうりゅう", "q": "からだが おおきくて 首がながいのは？", "a": "ぶらきおさうるす", "img": "🦕"}

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
        st.success(f"あたり！「{q['a']}」だよ")
