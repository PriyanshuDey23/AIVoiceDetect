import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure the Gemini API
genai.configure(api_key=os.getenv(GOOGLE_API_KEY))

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  
    generation_config=generation_config,
)

def upload_audio():
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac"])
    return uploaded_file

def detect_audio_type(audio_file):
    # Convert the uploaded audio file into a readable format for the model
    audio_bytes = audio_file.getvalue()
    
    # Use the audio file content to send a request to Gemini model
    chat_session = model.start_chat(history=[])
    message = f"Analyze the following audio to detect if it is AI-generated or voice-generated. Audio data: {audio_bytes}"

    response = chat_session.send_message(message)
    
    return response.text.strip()

def main():
    st.title("AI vs Voice Audio Detection ")

    uploaded_audio = upload_audio()

    if uploaded_audio is not None:
        st.audio(uploaded_audio, format="audio/wav")
        
        
        with st.spinner('Detecting audio type...'):
            result = detect_audio_type(uploaded_audio)
        
        # Display the result to the user
        if "AI-generated" in result:
            st.write("This audio is detected as AI-generated.")
        elif "Voice-generated" in result:
            st.write("This audio is detected as voice-generated.")
        else:
            st.write("Could not determine the audio type.")
    else:
        st.write("Please upload an audio file to get started.")

if __name__ == "__main__":
    main()
