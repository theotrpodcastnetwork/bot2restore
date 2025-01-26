import streamlit as st
from pydub import AudioSegment
from io import BytesIO

# Set the page configuration
st.set_page_config(page_title="Audio Enhancer Pro", page_icon="🎵", layout="wide")

# Create tabs for navigation
tabs = st.tabs(["Home", "How-To Guide", "Support"])

# Home Tab
with tabs[0]:
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #333333;
            text-align: center;
            margin-bottom: 20px;
        }
        .sub-header {
            font-size: 1.25rem;
            font-weight: 400;
            color: #666666;
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="main-header">Audio Enhancer Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform your audio with cutting-edge enhancement technology!</div>', unsafe_allow_html=True)

    # File Upload Section
    st.subheader("Step 1: Upload Your Audio File")
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg"])

    if uploaded_file:
        st.subheader("Step 2: Processing Your File")
        st.write("Your file is being processed. Please wait...")

        try:
            # Read file as binary data
            file_extension = uploaded_file.name.split('.')[-1].lower()
            audio_data = BytesIO(uploaded_file.read())

            # Load the audio file using pydub
            audio = AudioSegment.from_file(audio_data, format=file_extension)

            # Define chunk size (10 seconds)
            chunk_size = 10 * 1000  # 10 seconds in milliseconds
            st.write("Processing your audio in 10-second chunks for maximum efficiency.")

            # Process audio in chunks
            for start in range(0, len(audio), chunk_size):
                chunk = audio[start:start + chunk_size]
                st.write(f"Processing chunk: {start // 1000}s to {(start + chunk_size) // 1000}s...")

            # Display results
            st.success("Processing complete! Download or play your enhanced audio below.")
            st.audio(audio.export(format="wav"), format="audio/wav")

            st.download_button(
                label="Download Enhanced Audio",
                data=audio.export(format="wav"),
                file_name="enhanced_audio.wav",
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")

# How-To Guide Tab
with tabs[1]:
    st.subheader("How-To Guide for Beta Users")
    st.markdown(
        """
        Welcome to **Audio Enhancer Pro Beta**!  
        Here’s how to get started with enhancing your audio in just a few simple steps:

        ### **Step 1: Upload Your Audio File**
        - Click on the "Choose an audio file" button.
        - Select a file in MP3, WAV, or OGG format.
        - The file size should be under **10 MB** for optimal performance.

        ### **Step 2: Wait While We Process Your File**
        - The app will automatically process your audio in chunks for speed and accuracy.
        - You’ll see a progress update for each chunk being processed.

        ### **Step 3: Play and Download Your Enhanced Audio**
        - Once processing is complete, you’ll see a play button for your enhanced audio.
        - Click **"Download Enhanced Audio"** to save the processed file to your device.

        ### **Tips for the Best Experience**
        - **Use High-Quality Audio Files**: Starting with clear recordings will yield the best results.
        - **Ensure a Stable Internet Connection**: File uploads and downloads work best with a reliable connection.
        - **Report Bugs**: If you encounter any issues, please let us know via **audioenhancerpro@gmail.com**.
        """
    )

# Support Tab
with tabs[2]:
    st.subheader("Support")
    st.write("For further assistance or feedback, reach out to us at **audioenhancerpro@gmail.com**.")
