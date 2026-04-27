import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# カギの設定
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- クイズを新しく作る関数 ---
def create_new_quiz():
    # 2026年現在、最も安定しているモデル名です
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # AIに「絶対にこの形(JSON)で答えて」と念押しする設定
    prompt = "4歳向けのクイズ（恐竜、妖怪、動物のどれか）を1問作って。必ず以下のJSON形式だけで出力して。挨拶や解説は厳禁。 {'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
    
    try:
        # generation_configで「JSONで返せ」と強制します
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        # 返ってきたデータを辞書形式に変換
        return json.loads(response.text)
    except:
        # もしAIが失敗した時のための「第2予備問題」
        return {"genre": "きょうりゅう", "q": "からだが とっても おおきくて、くびが ながーいのだーれだ？", "a": "ぶらきおさうるす", "img": "🦕"}

st.title("🦖 AIむげんクイズ 👻")

# --- 「つぎへ」ボタン ---
if st.button("🌟 新しい もんだいにする"):
    st.session_state.quiz = create_new_quiz()
    st.rerun()

# 初回の準備
if 'quiz' not in st.session_state:
    st.session_state.quiz = create_new_quiz()

q = st.session_state.quiz

# --- 画面の表示 ---
st.info(f"ジャンル： {q['genre']}")
st.subheader(q['q'])

if st.button("🔊 こえを きく"):
    gTTS(q['q'], lang='ja').save("q.mp3")
    st.audio("q.mp3")

ans = st.text_input("こたえは なあに？", key="input_field")

if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！「{q['a']}」だよ {q['img']}")
    else:
        st.error("おしい！もういちど！")
