import streamlit as st
from gtts import gTTS
import random

st.title("🦖 ばあばの むげんクイズ 👻")

# ばあばが用意したクイズリスト（ここならカギ不要で動きます！）
def get_bakasan_quiz():
    quizzes = [
        {"genre": "どうぶつ", "q": "おはなが ながーいのだーれだ？", "a": "ぞう", "img": "🐘"},
        {"genre": "きょうりゅう", "q": "おなかが すくと ほえる、きょうりゅうの おうさまは？", "a": "てぃらのさうるす", "img": "🦖"},
        {"genre": "ようかい", "q": "あたまに おさらが のっているのは？", "a": "かっぱ", "img": "🥒"},
        {"genre": "どうぶつ", "q": "ぴょんぴょん はねる、おみみが ながいこは？", "a": "うさぎ", "img": "🐰"}
    ]
    return random.choice(quizzes)

if st.button("🌟 つぎのもんだい"):
    st.session_state.my_quiz = get_bakasan_quiz()
    st.rerun()

if 'my_quiz' not in st.session_state:
    st.session_state.my_quiz = get_bakasan_quiz()

q = st.session_state.my_quiz

st.info(f"ジャンル：{q['genre']}")
st.subheader(q['q'])

if st.button("🔊 こえを きく"):
    gTTS(q['q'], lang='ja').save("q.mp3")
    st.audio("q.mp3")

ans = st.text_input("こたえは？")
if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！ {q['a']} だよ！ {q['img']}")
