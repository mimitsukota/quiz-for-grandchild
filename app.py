import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json
import re

# カギの準備
try:
    # Secretsからカギを読み込む
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("カギの設定が見つかりません。Secretsを確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# AIにクイズを作らせる
def get_quiz():
    # 2026年の標準的なモデル名に修正しました
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = "4歳向けクイズ（恐竜、妖怪、動物）を1問作って。必ず以下のJSON形式だけで答えて： {'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
    
    try:
        response = model.generate_content(prompt)
        # AIの返事から {} の部分だけを抽出
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if match:
            # 安全に辞書形式に変換
            import ast
            return ast.literal_eval(match.group())
        else:
            raise Exception("形式エラー")
    except:
        # 万が一AIが失敗した時の予備問題
        return {"genre": "どうぶつ", "q": "おはなが ながーいのだーれだ？", "a": "ぞう", "img": "🐘"}

# クイズの保持
if 'quiz' not in st.session_state:
    with st.spinner('AIが クイズを かんがえ中...'):
        st.session_state.quiz = get_quiz()

q = st.session_state.quiz

st.header(f"ジャンル：{q['genre']}")
st.write(f"### {q['q']}")

if st.button("🔊 こえを きく"):
    try:
        gTTS(q['q'], lang='ja').save("q.mp3")
        st.audio("q.mp3")
    except:
        st.write("ごめんね、おんせいが 出せなかったよ。")

ans = st.text_input("こたえは？（ひらがな）")
if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！ {q['a']} だよ！ {q['img']}")
        if st.button("つぎへ"):
            del st.session_state.quiz
            st.rerun()
    elif ans == "":
        st.write("なにか かいてみてね！")
    else:
        st.error("ざんねん！もういちど かんがえてみてね。")
