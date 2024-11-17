import streamlit as st
import os
from gtts import gTTS
import tempfile
import base64
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Text to Speech Generator",
    page_icon="🎙️",
    layout="wide"
)

# Title and description
st.title("🎙️ Professional Text-to-Speech Generator")
st.markdown("Create high-quality audio content for your YouTube channel")

def text_to_speech(text, filename):
    """Simple TTS conversion without audio processing"""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)
    return filename

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# Main content area
tabs = st.tabs(["Single Story", "Batch Processing"])

with tabs[0]:
    st.header("Single Story Generator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        story_title = st.text_input("Story Title", "My Story")
        story_text = st.text_area(
            "Enter your story text",
            height=300,
            placeholder="Once upon a time..."
        )

    with col2:
        st.subheader("Voice Settings")
        
        speed = st.slider(
            "Speech Speed",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1
        )

    if st.button("Generate Audio", type="primary"):
        if story_text:
            with st.spinner("Generating audio..."):
                try:
                    # Create temporary directory
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Generate output filename
                        output_file = os.path.join(temp_dir, f"{story_title}.mp3")
                        
                        # Generate audio
                        text_to_speech(story_text, output_file)
                        
                        # Display audio player
                        audio_file = open(output_file, 'rb')
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        # Download button
                        st.markdown(
                            get_binary_file_downloader_html(output_file, 'Download Audio'),
                            unsafe_allow_html=True
                        )
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter some text to generate audio.")

with tabs[1]:
    st.header("Batch Story Processing")
    
    uploaded_files = st.file_uploader(
        "Upload text files (.txt)",
        type=['txt'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Process All Stories", type="primary"):
            with st.spinner("Processing stories..."):
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        for uploaded_file in uploaded_files:
                            # Read content
                            content = uploaded_file.read().decode()
                            
                            # Generate audio file name
                            file_name = os.path.splitext(uploaded_file.name)[0]
                            output_file = os.path.join(temp_dir, f"{file_name}.mp3")
                            
                            # Generate audio
                            text_to_speech(content, output_file)
                            
                            # Display results
                            st.subheader(file_name)
                            audio_file = open(output_file, 'rb')
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format='audio/mp3')
                            st.markdown(
                                get_binary_file_downloader_html(output_file, f'Download {file_name}'),
                                unsafe_allow_html=True
                            )
                            
                except Exception as e:
                    st.error(f"An error occurred during batch processing: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <p>Created for professional YouTube content creation</p>
    </div>
    """,
    unsafe_allow_html=True
)
