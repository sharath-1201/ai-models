import streamlit as st
import cohere

# Initialize Cohere API
COHERE_API_KEY = ""  # Replace with your API key
co = cohere.Client(COHERE_API_KEY)

# Streamlit App
st.title("AI Story Generator")
st.subheader("Generate a story from your imagination!")

# Input prompt
prompt = st.text_area("Enter your story prompt:", height=200)

# Story length selection
story_length = st.radio("Select story length:", ["Short", "Medium", "Long"])

# Map story length to tokens
length_map = {
    "Short": 100,
    "Medium": 300,
    "Long": 500
}
max_tokens = length_map[story_length]

# Generate Story Button
if st.button("Generate Story"):
    if prompt.strip():
        with st.spinner("Generating your story..."):
            try:
                # Generate story using Cohere
                response = co.generate(
                    model="command-xlarge-nightly",  # Use the Cohere command model
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=0.8,  # Adjust for creativity
                    k=0,
                    p=0.75,
                    stop_sequences=["--"]  # Optional: Add custom stop sequences
                )
                story = response.generations[0].text.strip()
                st.success("Here's your story!")
                st.write(story)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a prompt to generate the story.")
