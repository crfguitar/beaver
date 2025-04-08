
import streamlit as st
import whisper
import tempfile
import os
import random

st.set_page_config(page_title="Whisper: Beaver Edition")

model = whisper.load_model("base")

def beaverify(text):
    keyword_map = {
        "love": "respect for beaver society",
        "fight": "dam dispute",
        "build": "construct a dam",
        "family": "beaver colony",
        "river": "beaver highway",
        "city": "dam metropolis",
        "tree": "snack supply",
        "man": "beaver enthusiast",
        "woman": "beaver biologist",
    }
    for word, beaver_word in keyword_map.items():
        text = text.replace(word, beaver_word)
    facts = [
        "Beavers have transparent eyelids so they can see underwater.",
        "A beaver’s teeth never stop growing.",
        "Beaver dams can be seen from space.",
        "The largest beaver dam is over 850 meters long.",
    ]
    text += "\n\nBonus Beaver Fact: " + random.choice(facts)
    return text

st.title("Whisper: Beaver Edition")
st.write("Upload a song or recording and I’ll gently rewrite it to be about beavers.")

uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Transcribing with Whisper...")
    result = model.transcribe(tmp_path)
    original = result["text"]
    beaver_version = beaverify(original)

    st.subheader("Original Transcript")
    st.text_area("Original", original, height=200)

    st.subheader("Beaverfied Transcript")
    st.text_area("Beaver Edition", beaver_version, height=200)

    st.download_button("Download Beaver Lyrics", beaver_version, file_name="beaver_lyrics.txt")

    os.remove(tmp_path)
