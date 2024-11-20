import cohere
import streamlit as st

# Set your Cohere API key directly
cohere_api_key = ""

# Function to get response using Cohere's API
def get_cohere_response(question):
    # Initialize Cohere client
    co = cohere.Client(cohere_api_key)

    # Use Cohere to generate a response
    response = co.generate(
        model='command',  # You can change this to any available Cohere model
        prompt=question,
        max_tokens=100,
        temperature=0.5
    )
    
    return response.generations[0].text.strip()

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("LangChain Application with Cohere")

# User input
input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If ask button is clicked
if submit and input_text:
    response = get_cohere_response(input_text)
    st.subheader("The Response is")
    st.write(response)
