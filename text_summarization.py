import streamlit as st
import cohere

# Initialize Cohere API
COHERE_API_KEY = ""  # Replace with your API key
co = cohere.Client(COHERE_API_KEY)

# Streamlit App
st.title("Text Summarization with Cohere")

# Text Input
text_input = st.text_area("Enter text to summarize", height=200)
summary_length=st.radio(
                    "Select summary length:",
                    options=['short','medium','long'],
                    index=1
                )
if st.button("Summarize"):
    if text_input.strip():
        with st.spinner("Summarizing..."):
            try:
                response = co.summarize(
                    text=text_input,
                    length=summary_length,  # Options: "short", "medium", "long"
                    format="paragraph",  # Options: "paragraph", "bullet"
                    model="summarize-xlarge",  # Adjust based on your Cohere plan
                )
                st.success("Summary:")
                st.write(response.summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter some text to summarize.")
