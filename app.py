
import streamlit as st
from gtts import gTTS
import random
import time

st.title("🦖 おまごちゃんクイズ 👻")

quiz_data = [
    {"genre": "恐竜", "q": "ガオー！僕は恐竜の王様だ！鋭い牙があるよ。だーれだ？", "a": "ティラノサウルス", "img": "🦖"},
    {"genre": "妖怪", "q": "頭にお皿があって、キュウリが大好きなのだーれだ？", "a": "カッパ", "img": "🥒"},
    {"genre": "動物園", "q": "パオーン！お鼻が長くてお耳が大きいよ。だーれだ？", "a": "ゾウ", "img": "🐘"}
]

random.seed(time.strftime("%Y%m%d"))
quiz = random.choice(quiz_data)

st.header(f"ジャンル： {quiz['genre']}")

if st.button("🔊 もんだいを きく"):
    tts = gTTS(quiz['q'], lang='ja')
    tts.save("q.mp3")
    st.audio("q.mp3")

answer = st.text_input("こたえは？")
if st.button("こたえあわせ"):
    if answer in quiz['a']:
        st.balloons()
        st.success(f"せいかい！ {quiz['a']}")
        st.write(f"# {quiz['img']}")
