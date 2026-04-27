import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json
import re

# カギの準備
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("カギ（APIキー）の設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# AIにクイズを作らせる
def get_quiz():
    model = genai.GenerativeModel('gemini-1.5-flash')
    # AIに「余計なことは言わないで」と強く命令
    prompt = "4歳向けクイズを1問作って。形式は必ずこれだけ： {'genre': '動物', 'q': '問題', 'a': '答え', 'img': '絵文字'}"
    response = model.generate_content(prompt)
    
    # AIの返事から { } の部分だけを抜き出す魔法
    res_text = response.text
    match = re.search(r"\{.*\}", res_text, re.DOTALL)
    if match:
        # JSONとして読み込む（シングルクォートも許容する設定）
        quiz_data = eval(match.group())
        return quiz_data
    else:
        # 万が一の予備問題
        return {"genre":"どうぶつ","q":"おはながながいのだーれだ？","a":"ぞう","img":"🐘"}

# クイズを画面に出す
if 'quiz' not in st.session_state:
    st.session_state.quiz = get_quiz()

q = st.session_state.quiz

st.header(f"ジャンル：{q['genre']}")
st.subheader(q['q'])

if st.button("🔊 こえを きく"):
    gTTS(q['q'], lang='ja').save("q.mp3")
    st.audio("q.mp3")

ans = st.text_input("こたえは？")
if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！ {q['a']} だよ {q['img']}")
        if st.button("つぎへ"):
            del st.session_state.quiz
            st.rerun()
    else:
        st.error("ざんねん！もういちど！")
