def load_css():
    return """
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
    """ 