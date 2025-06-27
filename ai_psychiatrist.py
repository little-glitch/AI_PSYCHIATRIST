import streamlit as st
from openai import OpenAI

# Page styling with Streamlit
st.set_page_config(page_title="Bright Mind", page_icon="🧠", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #FFFDD0, #F5F5DC);
            font-family: 'Arial', sans-serif;
            color: #4A4A4A; /* Dark gray for text */
        }
        .stChatMessage {
            border-radius: 15px; 
            margin: 10px 0; 
            padding: 15px;
            font-size: 16px;
            max-width: 80%;
        }
        .stChatMessage.user { 
            background-color: #D2B48C; /* Tan color for user messages */
            color: white;
            text-align: right; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-left: auto;
        }
        .stChatMessage.assistant { 
            background-color: #FAFAD2; /* Light cream for assistant messages */
            color: #4A4A4A; /* Dark gray for text */
            text-align: left; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-right: auto;
        }
        .stButton>button { 
            background-color: #D2B48C; /* Tan color for buttons */
            color: white; 
            border-radius: 8px; 
            padding: 12px 20px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover { 
            background-color: #C4A484; /* Slightly darker tan for hover */
        }
        .stTextInput>div>div>input { 
            border-radius: 8px; 
            border: 2px solid #D2B48C; /* Tan border for input */
            padding: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        .stTextInput>div>div>input:focus { 
            border-color: #C4A484; /* Slightly darker tan for focus */
        }
        .stCaption { 
            color: #4A4A4A; /* Dark gray for captions */
            font-style: italic; 
            font-size: 18px; 
            text-align: center;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #FFFDD0, #F5F5DC); /* Cream gradient for sidebar */
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .sidebar .sidebar-content h2 {
            color: #4A4A4A; /* Dark gray for sidebar headings */
            font-size: 24px;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content p {
            color: #4A4A4A; /* Dark gray for sidebar text */
            font-size: 16px;
            line-height: 1.6;
        }
        /* Update green and red colors to cream-like tones */
        .stTitle h1 {
            color: #4A4A4A; /* Dark gray for title */
        }
        .stMarkdown strong {
            color: #D2B48C; /* Tan for bold text */
        }
        .stMarkdown a {
            color: #C4A484; /* Slightly darker tan for links */
        }
        /* Custom styling for the name and age input form */
        .stForm {
            background: linear-gradient(135deg, #FFFDD0, #F5F5DC);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stForm h3 {
            color: #4A4A4A;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .stForm label {
            color: #4A4A4A;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for additional information and controls
with st.sidebar:
    st.markdown("## About Bright Mind")
    st.markdown("""
        Welcome to **Bright Mind**! This application is designed to provide emotional support, guidance, and advice with empathy and professionalism. 
        Whether you're feeling stressed, anxious, or just need someone to talk to, Bright Mind is here to help.
    """)
    st.markdown("---")
    st.markdown("### Settings")
    st.markdown("Adjust the settings below to customize your experience.")
    temperature = st.slider("Response Temperature", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    st.markdown("---")
    st.markdown("### Disclaimer")
    st.markdown("""
        This application is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
    """)

# Main content area
st.markdown(
    "<h1 style='color: #D2B48C; text-align: center;'>Bright Mind 🧠</h1>", 
    unsafe_allow_html=True
)
st.caption("Providing emotional support, guidance, and empathy.")

# Set OpenAI API key and base URL
OPENAI_API_KEY = "token-abc123"
OPENAI_API_BASE = "http://localhost:8000/v1"

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
models = client.models.list()
model_name = models.data[0].id

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model_name

# Initialize session state for user info and messages
if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": None, "age": None}

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "You are an AI psychiatrist. Provide emotional support, guidance, and advice with empathy and professionalism. Keep responses brief and to the point. If the user requests more details, provide additional responses accordingly."
    }]

# Ask for user's name and age if not already provided
if not st.session_state.user_info["name"] or not st.session_state.user_info["age"]:
    with st.form("user_info_form"):
        st.markdown("### Welcome to Bright Mind! 🌟")
        name = st.text_input("What is your name?", placeholder="Enter your name")
        age = st.number_input("How old are you?", min_value=1, max_value=120, step=1)
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.user_info["name"] = name
            st.session_state.user_info["age"] = age
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Hello {name}! I'm here to listen and help. What's on your mind?"
            })
            st.rerun()

# Display messages (excluding the system message)
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip displaying the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is on your mind today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Include user's name in the prompt for personalization
        personalized_prompt = f"{st.session_state.user_info['name']}, {prompt}"
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
            temperature=temperature,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})    