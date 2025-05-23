import streamlit as st
import requests
import tempfile
import os
import random
from pydub import AudioSegment
import wave

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

def trim_wav_raw(input_path, output_path, max_duration_sec=20):
    with wave.open(input_path, "rb") as wf:
        framerate = wf.getframerate()
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        max_frames = int(framerate * max_duration_sec)

        params = wf.getparams()
        frames = wf.readframes(max_frames)

    with wave.open(output_path, "wb") as out_wav:
        out_wav.setnchannels(n_channels)
        out_wav.setsampwidth(sampwidth)
        out_wav.setframerate(framerate)
        out_wav.writeframes(frames)


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

    bbq_map = {
        "pork ribs": "premium gnaw bones",
        "pork": "birch bark strips",
        "ribs": "gnaw bones",
        "beans": "swamp legumes",
        "barbecue": "smoke-dried alder mash",
        "brisket": "oak slab roast",
        "sandwich": "mosswich",
        "spaghetti": "stringy vine pasta",
    }

    idioms = [
        "You can't dam a feeling.",
        "Chew fast, chew true.",
        "Even beavers need rest after a good flood.",
        "He who gathers twigs early gnaws longest.",
    ]

    # Combine maps based on mode
    if mode == "Beaver Gospel":
        wordmap = {**base_map, **gospel_additions, **bbq_map}
    elif mode == "DAMaged Chaos":
        wordmap = {**base_map, **chaos_additions, **bbq_map}
    else:
        wordmap = {**base_map, **bbq_map}

    # Priority: longest words first (avoid partial overlaps like 'pork ribs' before 'pork')
    for key in sorted(wordmap, key=len, reverse=True):
        val = wordmap[key]
        text = text.replace(f" {key} ", f" {val} ")

    # Add beaver idioms if not in Casual
    if mode != "Casual Naturalist":
        text += "\n\n" + "\n".join(random.sample(idioms, k=2))

    # Bonus Fact!
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
            trim_wav_raw(tmp_path, trimmed_path)
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


