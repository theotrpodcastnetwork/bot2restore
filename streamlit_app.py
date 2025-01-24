import streamlit as st
streamlit run streamlit_app.py
import os
import numpy as np
import librosa
import streamlit as st
from scipy.io.wavfile import write
import noisereduce as nr
from pydub import AudioSegment
import shutil

# Ensure output folder exists
OUTPUT_FOLDER = "ProcessedAudio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to split audio into chunks
def split_audio(file_path, chunk_duration=30):
    audio, sr = librosa.load(file_path, sr=None)
    total_duration = librosa.get_duration(y=audio, sr=sr)
    chunks = []

    for i in range(0, int(total_duration), chunk_duration):
        start = i * sr
        end = min((i + chunk_duration) * sr, len(audio))
        chunks.append(audio[start:end])

    return chunks, sr

# Process audio chunks
def process_chunks(chunks, sr, noise_strength, amp_level, norm_level, progress_bar):
    processed_chunks = []
    for i, chunk in enumerate(chunks):
        chunk = reduce_noise(chunk, sr, noise_strength)
        chunk = normalize_audio(chunk, norm_level)
        chunk = chunk * amp_level
        chunk = np.clip(chunk, -1.0, 1.0)
        processed_chunks.append(chunk)
        progress_bar.progress((i + 1) / len(chunks))
    return np.concatenate(processed_chunks)

# Noise reduction function
def reduce_noise(audio, sr, noise_reduction_strength):
    noise_sample = audio[:sr]
    return nr.reduce_noise(y=audio, sr=sr, y_noise=noise_sample, prop_decrease=noise_reduction_strength)

# Normalize audio
def normalize_audio(audio, normalization_level):
    max_amp = np.max(np.abs(audio))
    return audio / max_amp * normalization_level

# Restore and remaster audio with chunking
def restore_and_remaster(file_path, noise_strength, amp_level, norm_level):
    chunks, sr = split_audio(file_path)
    progress_bar = st.progress(0)
    processed_audio = process_chunks(chunks, sr, noise_strength, amp_level, norm_level, progress_bar)
    output_file_name = f"final_{os.path.basename(file_path)}"
    output_path = os.path.join(OUTPUT_FOLDER, output_file_name)
    write(output_path, sr, (processed_audio * 32767).astype(np.int16))
    return output_path

# Convert audio format
def convert_audio(input_path, output_format):
    audio = AudioSegment.from_file(input_path)
    output_path = input_path.replace(".wav", f".{output_format}")
    audio.export(output_path, format=output_format)
    return output_path

# Streamlit UI
st.set_page_config(page_title="Audio Enhancer Pro", page_icon="🎵", layout="wide")

# Header Section
st.markdown(
    """
    <style>
    body { background-color: #f9fafb; color: #333333; font-family: 'Inter', sans-serif; }
    .main-header { font-size: 3rem; font-weight: 800; color: #FF6600; text-align: center; margin-bottom: 1rem; }
    .sub-header { font-size: 1.25rem; color: #6b7280; text-align: center; margin-bottom: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header">Audio Enhancer Pro</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Restore and remaster your audio files with ease. Perfect for podcasters, musicians, and professionals.</div>',
    unsafe_allow_html=True,
)

# File Upload Section
uploaded_files = st.file_uploader(
    "Upload your audio files (MP3, WAV, FLAC)", type=["mp3", "wav", "flac"], accept_multiple_files=True
)

# Sidebar: Processing Settings
st.sidebar.header("Processing Settings")
preset = st.sidebar.selectbox("Choose a Preset", ["Custom", "Podcast", "Music", "Meeting Recording"])
if preset == "Podcast":
    noise_reduction_strength = 0.7
    amplification_level = 1.2
    normalization_level = 1.0
elif preset == "Music":
    noise_reduction_strength = 0.5
    amplification_level = 1.1
    normalization_level = 1.0
elif preset == "Meeting Recording":
    noise_reduction_strength = 0.9
    amplification_level = 1.5
    normalization_level = 0.8
else:
    noise_reduction_strength = st.sidebar.slider("Noise Reduction Strength", 0.1, 1.0, 0.5, step=0.1)
    amplification_level = st.sidebar.slider("Amplification Level", 0.5, 2.0, 1.0, step=0.1)
    normalization_level = st.sidebar.slider("Normalization Level", 0.5, 2.0, 1.0, step=0.1)

download_format = st.sidebar.radio("Download Format", ["WAV", "MP3"])

# Process Uploaded Files
if uploaded_files:
    temp_folder = "TempAudio"
    os.makedirs(temp_folder, exist_ok=True)

    for uploaded_file in uploaded_files:
        temp_file_path = os.path.join(temp_folder, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        restored_path = restore_and_remaster(
            file_path=temp_file_path,
            noise_strength=noise_reduction_strength,
            amp_level=amplification_level,
            norm_level=normalization_level,
        )

        if download_format == "MP3":
            restored_path = convert_audio(restored_path, "mp3")

        st.success(f"File processed successfully: {os.path.basename(restored_path)}")
        with open(restored_path, "rb") as processed_file:
            st.download_button(
                label=f"💾 Download {download_format.upper()}",
                data=processed_file,
                file_name=os.path.basename(restored_path),
                mime="audio/mpeg" if download_format == "MP3" else "audio/wav",
            )

    shutil.rmtree(temp_folder)
else:
    st.info("Please upload at least one audio file to proceed.")

# Footer Section
st.markdown('<div style="text-align: center;">Built with ❤️ for audio creators. © 2025 Audio Enhancer Pro</div>', unsafe_allow_html=True)
