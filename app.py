import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import ast
import re

# カギの準備
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("カギの設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def get_quiz():
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = "4歳向けクイズ（恐竜、妖怪、動物）を1問作って。必ず以下の形式のデータだけを返して： {'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
    
    try:
        response = model.generate_content(prompt)
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if match:
            # AIの答えを辞書形式に変換
            return ast.literal_eval(match.group())
        else:
            raise Exception()
    except:
        return {"genre": "どうぶつ", "q": "おはなが ながーいのだーれだ？", "a": "ぞう", "img": "🐘"}

# クイズを管理する仕組み
if 'quiz' not in st.session_state:
    st.session_state.quiz = get_quiz()

q = st.session_state.quiz

st.header(f"ジャンル：{q['genre']}")
st.subheader(q['q'])

# 音声ボタン
if st.button("🔊 もんだいを きく"):
    gTTS(q['q'], lang='ja').save("q.mp3")
    st.audio("q.mp3")

ans = st.text_input("こたえは なあに？", key="input_text")

# 判定と「つぎへ」ボタン
if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
        
        # ここで「つぎのもんだい」を作る準備をする
        if st.button("🌟 つぎのもんだいに いく！"):
            del st.session_state.quiz
            st.rerun()
    elif ans == "":
        st.info("なにか かいてみてね！")
    else:
        st.error("おしい！もういちど かんがえてみてね。")

# 強制的に次の問題に変えるボタン（右下に配置）
st.write("---")
if st.button("ちがう もんだいに かえる"):
    del st.session_state.quiz
    st.rerun()
