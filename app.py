import streamlit as st
import openai
from typing import List, Dict
import time
import sentry_sdk

# Initialize Sentry at the top of your app
sentry_sdk.init(
    dsn=st.secrets["SENTRY_DSN"],  # Get DSN from your secrets
    
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    profiles_sample_rate=1.0,
    
    # Enable performance monitoring
    enable_tracing=True,
    
    # Add environment tag
    environment="development"  # or "production" based on your setup
)

class Message:
    def __init__(self, content: str, role: str):
        self.content = content
        self.role = role

class ChatBot:
    def __init__(self):
        try:
            self.client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            # Initialize with default model, will be updated via sidebar selection
            self.model = "gpt-3.5-turbo"  # Default model, will be updated via sidebar
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e
    
    def generate_response(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        try:
            with sentry_sdk.start_span(op="openai_request", description="Generate AI Response"):
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                )
            return response.choices[0].message.content
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return f"Error: {str(e)}"

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'chat_bot' not in st.session_state:
        st.session_state.chat_bot = ChatBot()

def display_messages():
    """Display chat messages"""
    for message in st.session_state.messages:
        with st.chat_message(message.role):
            st.write(message.content)

def main():
    try:
        st.title("🤖 AI Chatbot")
        
        # Initialize session state
        initialize_session_state()
        
        # Add user context to Sentry
        sentry_sdk.set_user({"id": st.session_state.get("user_id", "anonymous")})
        
        # Sidebar for model selection
        model = st.sidebar.selectbox(
            "Choose a model",
            ["gpt-3.5-turbo", "gpt-4"],
            key="model_selector"
        )
        st.session_state.chat_bot.model = model
        
        # Temperature slider
        temperature = st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1
        )
        
        # Clear chat button
        if st.sidebar.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Display chat messages
        display_messages()
        
        # Chat input with error handling
        if prompt := st.chat_input("What's on your mind?"):
            with sentry_sdk.start_transaction(name="chat_interaction") as transaction:
                # Add user message
                st.session_state.messages.append(Message(prompt, "user"))
                with st.chat_message("user"):
                    st.write(prompt)
                
                # Generate and display assistant response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        with sentry_sdk.start_span(op="generate_response", description="Generate Response"):
                            response = st.session_state.chat_bot.generate_response(prompt)
                            st.write(response)
                st.session_state.messages.append(Message(response, "assistant"))
                
                transaction.finish()
                
    except Exception as e:
        sentry_sdk.capture_exception(e)
        st.error("An unexpected error occurred. Our team has been notified.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Chatbot",
        page_icon="🤖",
        layout="centered",
        # Add dark theme
        initial_sidebar_state="expanded"
    )
    
    # Updated custom CSS
    st.markdown("""
        <style>
        /* Dark theme for the main page */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Style for chat messages */
        .stChatMessage {
            background-color: #262730;
            border-radius: 15px;
            padding: 15px;
            margin: 5px 0;
        }
        
        /* User message specific style */
        .stChatMessage[data-testid="chat-message-user"] {
            background-color: #004D40;
        }
        
        /* Assistant message specific style */
        .stChatMessage[data-testid="chat-message-assistant"] {
            background-color: #1E1E1E;
        }
        
        /* Input box style */
        .stChatInputContainer {
            background-color: #262730;
            padding: 10px;
            border-radius: 10px;
        }
        
        /* Sidebar style */
        .css-1d391kg {
            background-color: #262730;
        }
        
        /* Button style */
        .stButton>button {
            background-color: #004D40;
            color: white;
            border-radius: 5px;
        }
        
        .stButton>button:hover {
            background-color: #00695C;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    main() 