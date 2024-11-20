import streamlit as st
from huggingface_hub import InferenceApi
from moviepy import editor as mp
import requests
from io import BytesIO

# Set up Hugging Face API
HF_API_KEY = ""  # Replace with your Hugging Face API Key
MODEL_ID = "CompVis/stable-diffusion-v1-4"  # You can replace this with another model ID if needed

# Streamlit App
st.title("Text-to-Video Generation with Hugging Face")
st.write("Generate a video from images created with Stable Diffusion.")

# Prompt Input
prompt = st.text_input("Enter a prompt for image generation:", "A beautiful landscape")

# Number of frames to generate
num_frames = st.slider("Select the number of frames for your video:", 10, 50, 20)

# Frames per second (FPS)
fps = st.slider("Frames per second (FPS):", 10, 30, 15)

# Function to generate image from Hugging Face API
def generate_image(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_ID}",
        headers=headers,
        json={"inputs": prompt}
    )
    if response.status_code == 200:
        image = response.content
        return image
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Generate Video Button
if st.button("Generate Video"):
    if prompt.strip():
        with st.spinner("Generating frames..."):
            try:
                # Create frames from the prompt
                frames = []
                for i in range(num_frames):
                    frame_prompt = f"{prompt}, frame {i+1} of {num_frames}"
                    img_bytes = generate_image(frame_prompt)
                    if img_bytes:
                        img = mp.editor.ImageClip(BytesIO(img_bytes)).set_duration(1 / fps)
                        frames.append(img)

                # Create video from frames
                video = mp.editor.concatenate_videoclips(frames, method="compose")
                video_path = "generated_video.mp4"
                video.write_videofile(video_path, codec="libx264")
                
                # Display video
                st.success("Video generated successfully!")
                st.video(video_path)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a prompt to generate the video.")
