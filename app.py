import streamlit as st
from configparser import ConfigParser
from chatbot import ChatBot

@st.cache_data  # Caches the results of this function
def get_chatbot_response(api_key, prompt):
    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()
    return chatbot.send_prompt(prompt)

def main():
    # Read the API key from credentials file
    config = ConfigParser()
    config.read('credentials.ini.txt')
    api_key = config['gemini_ai']['API_KEY']

    # Set up the session state for the conversation history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Initialize session state for input clearing
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0

    # Display the conversation history with adjusted text size and no extra lines
    st.write("<h3>Chatbot conversation:</h3>", unsafe_allow_html=True)
    for message in st.session_state.history:
        if message["role"] == "user":
            st.markdown(f"<p style='font-size:14px;'>You: {message['text'].strip()}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font-size:14px;'>MK Chatbot: {message['text'].strip()}</p>", unsafe_allow_html=True)

    # Input field for user prompt with a dynamic key
    user_input = st.text_input("You: ", key=f"user_input_{st.session_state.input_key}")

    # Functionality to handle chatbot response and update conversation history
    if st.button("Send") and user_input:
        try:
            # Get response from the chatbot
            response = get_chatbot_response(api_key, user_input)
            # Append user message and chatbot response to history
            st.session_state.history.append({"role": "user", "text": user_input})
            st.session_state.history.append({"role": "bot", "text": response.strip()})

            # Clear the input field by updating the key
            st.session_state.input_key += 1
            st.text_input("You: ", value="", key=f"user_input_{st.session_state.input_key}")  # Clear input field
        except Exception as e:
            st.error(f"Error: {e}")

# Run the chatbot app
if __name__ == "__main__":
    st.set_page_config(page_title="MK Chatbot", layout="centered")
    main()
