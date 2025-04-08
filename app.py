import streamlit as st
import requests
import tempfile
import os
import random
from pydub import AudioSegment

st.set_page_config(page_title="Whisper: Beaver Edition")

HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

MAX_MB = 25

def transcribe_with_whisper_api(audio_path):
    with open(audio_path, "rb") as f:
        response = requests.post(API_URL, headers=headers, data=f)
    if response.status_code != 200:
        raise Exception(f"Whisper API error: {response.status_code}\n{response.text}")
    return response.json().get("text", "")

def trim_audio(input_path, output_path, duration_ms=60000):
    audio = AudioSegment.from_file(input_path)
    trimmed = audio[:duration_ms]
    trimmed.export(output_path, format="wav")

def beaverify(text, mode="Casual Naturalist"):
    base_map = {
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

    gospel_additions = {
        "king": "grand beaver patriarch",
        "nation": "woodland dominion",
        "people": "fellow dam builders",
        "enemy": "log thief",
        "truth": "gnawed revelation",
    }

    chaos_additions = {
        "the": "THE (as in THE dam)",
        "a": "one glorious",
        "night": "moonlight dam shift",
        "light": "gnawbeam",
        "sound": "timbercore frequency",
    }

    idioms = [
        "You can't dam a feeling.",
        "Chew fast, chew true.",
        "Even beavers need rest after a good flood.",
        "He who gathers twigs early gnaws longest.",
    ]

    if mode == "Beaver Gospel":
        wordmap = {**base_map, **gospel_additions}
    elif mode == "DAMaged Chaos":
        wordmap = {**base_map, **chaos_additions}
    else:
        wordmap = base_map

    for key, val in wordmap.items():
        text = text.replace(f" {key} ", f" {val} ")

    if mode != "Casual Naturalist":
        text += "\n\n" + "\n".join(random.sample(idioms, k=2))

    text += "\n\nBonus Beaver Fact: " + random.choice([
        "Beavers slap their tails to warn others of danger.",
        "Beaver teeth are orange due to iron content.",
        "Beavers hate the sound of running water — they'll try to dam it.",
        "Beaver lodges have underwater entrances and cozy dens.",
    ])
    return text

st.title("Whisper: Beaver Edition")
st.write("Upload a song or voice recording, and this app will gently (or chaotically) rewrite it to be about beavers.")

flavor = st.selectbox("Choose your Beaver Mode", ["Casual Naturalist", "Beaver Gospel", "DAMaged Chaos"])

uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info(f"File size: {file_size_mb:.2f}MB")

    try:
        # Automatically trim if file is over HF limit
        if file_size_mb > MAX_MB:
            st.warning("File exceeds Hugging Face API size limit. Trimming to first 60 seconds...")
            trimmed_path = tmp_path.replace(".wav", "_trimmed.wav")
            trim_audio(tmp_path, trimmed_path)
            os.remove(tmp_path)
            tmp_path = trimmed_path

        st.info("Transcribing with Whisper API...")
        original = transcribe_with_whisper_api(tmp_path)
        beaver_version = beaverify(original, mode=flavor)

        st.subheader("Original Transcript")
        st.text_area("Original", original, height=200)

        st.subheader("Beaverfied Transcript")
        st.text_area("Beaver Edition", beaver_version, height=200)

        st.download_button("Download Beaver Lyrics", beaver_version, file_name="beaver_lyrics.txt")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


